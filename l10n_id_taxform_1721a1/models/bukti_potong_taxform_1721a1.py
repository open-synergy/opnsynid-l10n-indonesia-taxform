# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from datetime import datetime

from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.translate import _


class BuktiPotongTaxform1721A1(models.Model):
    _name = "l10n_id.bukti_potong_taxform_1721a1"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
        "custom.info.mixin",
    ]
    _description = "Bukti Potong Taxform 1721 A1"

    _state_from = ["draft", "confirm"]
    _state_to = ["done"]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_pemotong_pajak_id(self):
        return self.env.user.company_id.partner_id.id

    @api.model
    def _default_date(self):
        return datetime.now().strftime("%Y-%m-%d")

    @api.depends(
        "penghasilan_01",
        "penghasilan_02",
        "penghasilan_03",
        "penghasilan_04",
        "penghasilan_05",
        "penghasilan_06",
        "penghasilan_07",
    )
    @api.multi
    def _compute_penghasilan(self):
        for penghasilan in self:
            penghasilan.penghasilan_08 = 0.0
            penghasilan.penghasilan_08 = (
                penghasilan.penghasilan_01
                + penghasilan.penghasilan_02
                + penghasilan.penghasilan_03
                + penghasilan.penghasilan_04
                + penghasilan.penghasilan_05
                + penghasilan.penghasilan_06
                + penghasilan.penghasilan_07
            )

    @api.depends("penghasilan_08")
    @api.multi
    def _compute_jabatan(self):
        for jabatan in self:
            obj_biaya_jabatan = self.env["l10n_id.pph_21_biaya_jabatan"]
            perhitungan_biaya_jabatan = obj_biaya_jabatan.find(
                jabatan.date
            ).get_biaya_jabatan(
                0.0,
                jabatan.penghasilan_08,
                0,
                True,
            )
            jabatan.pengurang_09 = perhitungan_biaya_jabatan["biaya_jabatan_setahun"]

    @api.depends("pengurang_09", "pengurang_10")
    @api.multi
    def _compute_pengurang(self):
        for pengurang in self:
            pengurang.pengurang_11 = 0.0
            pengurang.pengurang_11 = pengurang.pengurang_09 + pengurang.pengurang_10

    @api.depends("penghasilan_08", "pengurang_11")
    @api.multi
    def _compute_penghasilan_netto(self):
        for pn in self:
            pn.perhitungan_12 = 0.0
            pn.perhitungan_12 = pn.penghasilan_08 - pn.pengurang_11

    @api.depends("perhitungan_12", "perhitungan_13")
    @api.multi
    def _compute_penghasilan_netto_setahun(self):
        for pns in self:
            pns.perhitungan_14 = 0.0
            pns.perhitungan_14 = pns.perhitungan_12 + pns.perhitungan_13

    @api.depends("wajib_pajak_ptkp_category_id", "date")
    @api.multi
    def _compute_ptkp(self):
        for getptkp in self:
            getptkp.perhitungan_15 = 0.0
            ptkp_category = getptkp.wajib_pajak_ptkp_category_id
            if ptkp_category:
                ptkp = ptkp_category.get_rate(getptkp.date)
                getptkp.perhitungan_15 = ptkp

    @api.depends(
        "perhitungan_14",
        "perhitungan_15",
    )
    @api.multi
    def _compute_pkp(self):
        for pkp in self:
            pkp.perhitungan_16 = 0.0
            if pkp.perhitungan_14 > pkp.perhitungan_15:
                pkp.perhitungan_16 = float(
                    int((pkp.perhitungan_14 - pkp.perhitungan_15) / 1000) * 1000
                )

    @api.depends(
        "perhitungan_16",
    )
    @api.multi
    def _compute_pph21(self):
        for pph in self:
            pph_21 = 0.0
            if pph.perhitungan_16 > 0:
                obj_pph = self.env["l10n_id.pph_21_rate"]
                pph_21 = obj_pph.find(pph.date).compute_tax(pph.perhitungan_16)
            pph.perhitungan_17 = pph_21

    @api.depends(
        "perhitungan_17",
        "perhitungan_18",
    )
    @api.multi
    def _compute_hutang_pph(self):
        for hutpph in self:
            hutpph.perhitungan_19 = hutpph.perhitungan_17 + hutpph.perhitungan_18

    name = fields.Char(
        string="# Form A1721 A1",
        required=True,
        default="/",
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    kode_objek_pajak_id = fields.Many2one(
        string="Kode Objek Pajak",
        comodel_name="l10n_id.taxform_objek_pajak",
        ondelete="restrict",
        required=True,
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=lambda self: self._default_date(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    tax_year_id = fields.Many2one(
        string="Tax Year",
        comodel_name="l10n_id.tax_year",
        compute=False,
        readonly=True,
        required=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    start_tax_period_id = fields.Many2one(
        string="Period Awal",
        comodel_name="l10n_id.tax_period",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    end_tax_period_id = fields.Many2one(
        string="Period Akhir",
        comodel_name="l10n_id.tax_period",
        compute=False,
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    pemotong_pajak_id = fields.Many2one(
        string="Pemotong Pajak",
        comodel_name="res.partner",
        required=True,
        ondelete="restrict",
        default=lambda self: self._default_pemotong_pajak_id(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    wajib_pajak_id = fields.Many2one(
        string="Wajib Pajak",
        comodel_name="res.partner",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    wajib_pajak_npwp = fields.Char(
        string="NPWP",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    wajib_pajak_alamat = fields.Char(
        string="Alamat",
        readonly=True,
        required=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    wajib_pajak_alamat2 = fields.Char(
        string="Alamat2",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    wajib_pajak_zip = fields.Char(
        string="ZIP",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    wajib_pajak_kota = fields.Char(
        string="Kota",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    wajib_pajak_state_id = fields.Many2one(
        string="State",
        comodel_name="res.country.state",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    wajib_pajak_country_id = fields.Many2one(
        string="Negara",
        comodel_name="res.country",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    wajib_pajak_nik = fields.Char(
        string="NIK",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    wajib_pajak_jenis_kelamin = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ],
        string="Jenis Kelamin",
        related="wajib_pajak_id.gender",
        store=False,
        readonly=True,
    )
    wajib_pajak_ptkp_category_id = fields.Many2one(
        string="PTKP Kategori",
        comodel_name="l10n_id.ptkp_category",
        readonly=True,
        required=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    wajib_pajak_job_position = fields.Char(
        string="Jabatan",
        readonly=True,
        required=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    wajib_pajak_karyawan_asing = fields.Boolean(
        string="Karyawan Asing",
        default=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    wajib_pajak_kode_negara = fields.Char(
        string="Kode Negara Domisili",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    penghasilan_01 = fields.Float(
        string="GAJI/PENSIUN ATAU THT/JHT",
        default=0.0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    penghasilan_02 = fields.Float(
        string="TUNJANGAN PPh",
        default=0.0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    penghasilan_03 = fields.Float(
        string="TUNJANGAN LAINNYA, UANG LEMBUR DAN SEBAGAINYA",
        default=0.0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    penghasilan_04 = fields.Float(
        string="HONORARIUM DAN IMBALAN LAIN SEJENISNYA",
        default=0.0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    penghasilan_05 = fields.Float(
        string="PREMI ASURANSI YANG DIBAYAR PEMBERI KERJA",
        default=0.0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    penghasilan_06 = fields.Float(
        string="PENERIMAAN DALAM BENTUK NATURA DAN KENIKMATAN \
           LAINNYA YANG DIKENAKAN PEMOTONGAN PPh PASAL 21",
        default=0.0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    penghasilan_07 = fields.Float(
        string="TANTIEM, BONUS, GRATIFIKASI, JASA PRODUKSI DAN THR",
        default=0.0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    penghasilan_08 = fields.Float(
        string="JUMLAH PENGHASILAN BRUTO (1 S.D. 7)",
        compute="_compute_penghasilan",
        store=True,
        readonly=True,
    )
    pengurang_09 = fields.Float(
        string="BIAYA JABATAN/BIAYA PENSIUN",
        compute="_compute_jabatan",
        store=True,
        readonly=True,
    )
    pengurang_10 = fields.Float(
        string="IURAN PENSIUN ATAU IURAN THT/JHT",
        default=0.0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    pengurang_11 = fields.Float(
        string="JUMLAH PENGURANGAN (9 S.D. 10)",
        compute="_compute_pengurang",
        store=True,
        readonly=True,
    )
    perhitungan_12 = fields.Float(
        string="JUMLAH PENGHASILAN NETO (8 ­ 11)",
        compute="_compute_penghasilan_netto",
        store=True,
        readonly=True,
    )
    perhitungan_13 = fields.Float(
        string="PENGHASILAN NETO MASA SEBELUMNYA",
        default=0.0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    perhitungan_14 = fields.Float(
        string="JUMLAH PENGHASILAN NETO UNTUK PENGHITUNGAN PPh \
            PASAL 21 (SETAHUN/DISETAHUNKAN)",
        compute="_compute_penghasilan_netto_setahun",
        store=True,
        readonly=True,
    )
    perhitungan_15 = fields.Float(
        string="PENGHASILAN TIDAK KENA PAJAK (PTKP)",
        compute="_compute_ptkp",
        store=True,
        readonly=True,
    )
    perhitungan_16 = fields.Float(
        string="PENGHASILAN KENA PAJAK SETAHUN/DISETAHUNKAN",
        compute="_compute_pkp",
        store=True,
        readonly=True,
    )
    perhitungan_17 = fields.Float(
        string="PPh PASAL 21 ATAS PENGHASILAN KENA PAJAK SETAHUN/DISETAHUNKAN",
        compute="_compute_pph21",
        store=True,
        readonly=True,
    )
    perhitungan_18 = fields.Float(
        string="PPh PASAL 21 YANG TELAH DIPOTONG MASA SEBELUMNYA",
        readonly=True,
        default=0.0,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    perhitungan_19 = fields.Float(
        string="PPh PASAL 21 TERUTANG",
        compute="_compute_hutang_pph",
        store=True,
        readonly=True,
    )
    perhitungan_20 = fields.Float(
        string="PPh PASAL 21 DAN PPh PASAL 26 YANG TELAH DIPOTONG DAN DILUNASI",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    ttd_id = fields.Many2one(
        string="TTD",
        comodel_name="res.partner",
        readonly=True,
        required=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        required=True,
        readonly=True,
    )
    confirm_date = fields.Datetime(
        string="Confirmation Date",
        readonly=True,
        copy=False,
    )
    confirm_user_id = fields.Many2one(
        string="Confirmed By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    done_date = fields.Datetime(
        string="Finish Date",
        readonly=True,
        copy=False,
    )
    done_user_id = fields.Many2one(
        string="Finished By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    cancel_date = fields.Datetime(
        string="Cancel Date",
        readonly=True,
        copy=False,
    )
    cancel_user_id = fields.Many2one(
        string="Cancelled By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    restart_approval_ok = fields.Boolean(
        string="Can Restart Approval",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )

    @api.multi
    def action_confirm(self):
        for record in self:
            record.write(record._prepare_confirm_data())
            record.request_validation()

    @api.multi
    def action_approve(self):
        for record in self:
            record.write(record._prepare_approve_data())

    @api.multi
    def action_cancel(self):
        for record in self:
            record.write(record._prepare_cancel_data())

    @api.multi
    def action_restart(self):
        for record in self:
            record.write(record._prepare_restart_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
            "confirm_date": fields.Datetime.now(),
            "confirm_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_approve_data(self):
        self.ensure_one()
        sequence = self._create_sequence()
        return {
            "state": "done",
            "done_date": fields.Datetime.now(),
            "done_user_id": self.env.user.id,
            "name": sequence,
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "done_date": False,
            "done_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
        }

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for record in self:
            if record.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(BuktiPotongTaxform1721A1, self)
        _super.unlink()

    @api.multi
    def validate_tier(self):
        _super = super(BuktiPotongTaxform1721A1, self)
        _super.validate_tier()
        for record in self:
            if record.validated:
                record.action_approve()

    @api.multi
    def restart_validation(self):
        _super = super(BuktiPotongTaxform1721A1, self)
        _super.restart_validation()
        for record in self:
            record.request_validation()

    def _get_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    @api.onchange("wajib_pajak_id")
    def onchange_wajib_pajak_id(self):
        if self.wajib_pajak_id:
            self.wajib_pajak_nik = self.wajib_pajak_id.ektp_number
            self.wajib_pajak_npwp = self.wajib_pajak_id.vat
            self.wajib_pajak_alamat = self.wajib_pajak_id.street
            self.wajib_pajak_alamat2 = self.wajib_pajak_id.street2
            self.wajib_pajak_zip = self.wajib_pajak_id.zip
            self.wajib_pajak_kota = self.wajib_pajak_id.city
            self.wajib_pajak_state_id = self.wajib_pajak_id.state_id
            self.wajib_pajak_country_id = self.wajib_pajak_id.country_id
            self.wajib_pajak_ptkp_category_id = self.wajib_pajak_id.ptkp_category_id
            self.wajib_pajak_job_position = self.wajib_pajak_id.function

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_penghasilan_01(self):
        self.penghasilan_01 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            try:
                eval(
                    self.company_id.python_code_1721a1_penghasilan_01,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
                result = localdict["result"]
            except Exception:
                result = 0.0
            self.penghasilan_01 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_penghasilan_02(self):
        self.penghasilan_02 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            try:
                eval(
                    self.company_id.python_code_1721a1_penghasilan_02,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
                result = localdict["result"]
            except Exception:
                result = 0.0
            self.penghasilan_02 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_penghasilan_03(self):
        self.penghasilan_03 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            try:
                eval(
                    self.company_id.python_code_1721a1_penghasilan_03,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
                result = localdict["result"]
            except Exception:
                result = 0.0
            self.penghasilan_03 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_penghasilan_04(self):
        self.penghasilan_04 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            try:
                eval(
                    self.company_id.python_code_1721a1_penghasilan_04,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
                result = localdict["result"]
            except Exception:
                result = 0.0
            self.penghasilan_04 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_penghasilan_05(self):
        self.penghasilan_05 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            try:
                eval(
                    self.company_id.python_code_1721a1_penghasilan_05,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
                result = localdict["result"]
            except Exception:
                result = 0.0
            self.penghasilan_05 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_penghasilan_06(self):
        self.penghasilan_06 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            try:
                eval(
                    self.company_id.python_code_1721a1_penghasilan_06,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
                result = localdict["result"]
            except Exception:
                result = 0.0
            self.penghasilan_06 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_penghasilan_07(self):
        self.penghasilan_07 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            try:
                eval(
                    self.company_id.python_code_1721a1_penghasilan_07,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
                result = localdict["result"]
            except Exception:
                result = 0.0
            self.penghasilan_07 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_pengurang_10(self):
        self.pengurang_10 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            try:
                eval(
                    self.company_id.python_code_1721a1_pengurang_10,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
                result = localdict["result"]
            except Exception:
                result = 0.0
            self.pengurang_10 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_perhitungan_13(self):
        self.perhitungan_13 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            try:
                eval(
                    self.company_id.python_code_1721a1_perhitungan_13,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
                result = localdict["result"]
            except Exception:
                result = 0.0
            self.perhitungan_13 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_perhitungan_18(self):
        self.perhitungan_18 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            try:
                eval(
                    self.company_id.python_code_1721a1_perhitungan_18,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
                result = localdict["result"]
            except Exception:
                result = 0.0
            self.perhitungan_18 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_perhitungan_20(self):
        self.perhitungan_20 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            try:
                eval(
                    self.company_id.python_code_1721a1_perhitungan_20,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
                result = localdict["result"]
            except Exception:
                result = 0.0
            self.perhitungan_20 = result
