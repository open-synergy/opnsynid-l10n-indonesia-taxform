# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.tools.safe_eval import safe_eval as eval

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError

from odoo.addons.ssi_decorator import ssi_decorator


class L10nIdBuktiPotongPph1721A1(models.Model):
    """
    Represents Indonesia's PPh 21 Withholding Slip Form 1721 A1.
    Computes gross income, deductions, PTKP, and the annual/annualized
    PPh 21 payable for a single taxpayer, through the standard
    confirm/approve/done workflow.
    """

    _name = "l10n_id.bukti_potong_pph_1721_a1"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.print_document",
    ]
    _description = "Bukti Potong PPh 21 1721 A1"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_button = False
    _automatically_insert_done_policy_fields = False

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    def _default_company_id(self):
        """Return the default ``company_id`` value.

        :return: id of the current user's company
        """
        return self.env.user.company_id.id

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
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=lambda self: fields.Date.today(),
        readonly=True,
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

    @api.model
    def _default_pemotong_pajak_id(self):
        """Return the default ``pemotong_pajak_id`` value.

        :return: id of the current company's partner
        """
        return self.env.user.company_id.partner_id.id

    pemotong_pajak_id = fields.Many2one(
        string="Pemotong Pajak",
        comodel_name="res.partner",
        required=True,
        ondelete="restrict",
        domain=[("is_company", "=", True)],
        default=lambda self: self._default_pemotong_pajak_id(),
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
            ("reject", "Rejected"),
        ],
        default="draft",
        copy=False,
    )

    # INFORMASI UMUM
    wajib_pajak_id = fields.Many2one(
        string="Wajib Pajak",
        comodel_name="res.partner",
        required=True,
        ondelete="restrict",
        readonly=True,
        domain=[
            ("is_company", "=", False),
            ("parent_id", "=", False),
        ],
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

    # PENGHASILAN
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
        compute_sudo=True,
    )

    # PENGURANG
    @api.depends("penghasilan_08")
    def _compute_jabatan(self):
        """Compute ``pengurang_09``, the annual occupational expense.

        Delegates to ``l10n_id.pph_21_biaya_jabatan`` to look up the
        occupational expense (biaya jabatan) rate that applies on the
        document date, applied to the gross income for the year.
        """
        for document in self:
            obj_biaya_jabatan = self.env["l10n_id.pph_21_biaya_jabatan"]
            perhitungan_biaya_jabatan = obj_biaya_jabatan.find(
                document.date
            ).get_biaya_jabatan(
                0.0,
                document.penghasilan_08,
                0,
                True,
            )
            document.pengurang_09 = perhitungan_biaya_jabatan["biaya_jabatan_setahun"]

    pengurang_09 = fields.Float(
        string="BIAYA JABATAN/BIAYA PENSIUN",
        compute="_compute_jabatan",
        store=True,
        readonly=True,
        compute_sudo=True,
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

    @api.depends(
        "pengurang_09",
        "pengurang_10",
    )
    def _compute_pengurang(self):
        """Compute ``pengurang_11``, the total deduction.

        Sums the occupational expense (``pengurang_09``) and the
        pension/JHT-THT contribution (``pengurang_10``).
        """
        for document in self:
            document.pengurang_11 = 0.0
            document.pengurang_11 = document.pengurang_09 + document.pengurang_10

    pengurang_11 = fields.Float(
        string="JUMLAH PENGURANGAN (9 S.D. 10)",
        compute="_compute_pengurang",
        store=True,
        readonly=True,
        compute_sudo=True,
    )

    # PERHITUNGAN
    @api.depends(
        "penghasilan_08",
        "pengurang_11",
    )
    def _compute_penghasilan_netto(self):
        """Compute ``perhitungan_12``, the net income for the period.

        Subtracts the total deduction (``pengurang_11``) from the gross
        income (``penghasilan_08``).
        """
        for document in self:
            document.perhitungan_12 = 0.0
            document.perhitungan_12 = document.penghasilan_08 - document.pengurang_11

    perhitungan_12 = fields.Float(
        string="JUMLAH PENGHASILAN NETO (8 ­ 11)",
        compute="_compute_penghasilan_netto",
        store=True,
        readonly=True,
        compute_sudo=True,
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

    @api.depends(
        "perhitungan_12",
        "perhitungan_13",
    )
    def _compute_penghasilan_netto_setahun(self):
        """Compute ``perhitungan_14``, the annualized net income.

        Adds the net income for the current period (``perhitungan_12``)
        to the net income already reported for prior periods
        (``perhitungan_13``).
        """
        for document in self:
            document.perhitungan_14 = 0.0
            document.perhitungan_14 = document.perhitungan_12 + document.perhitungan_13

    perhitungan_14 = fields.Float(
        string="JUMLAH PENGHASILAN NETO UNTUK PENGHITUNGAN PPh \
            PASAL 21 (SETAHUN/DISETAHUNKAN)",
        compute="_compute_penghasilan_netto_setahun",
        store=True,
        readonly=True,
        compute_sudo=True,
    )

    @api.depends(
        "wajib_pajak_ptkp_category_id",
        "date",
    )
    def _compute_ptkp(self):
        """Compute ``perhitungan_15``, the non-taxable income (PTKP).

        Looks up the PTKP rate for the taxpayer's PTKP category
        (``wajib_pajak_ptkp_category_id``) as of the document date.
        """
        for document in self:
            document.perhitungan_15 = 0.0
            ptkp_category = document.wajib_pajak_ptkp_category_id
            if ptkp_category:
                ptkp = ptkp_category.get_rate(document.date)
                document.perhitungan_15 = ptkp

    perhitungan_15 = fields.Float(
        string="PENGHASILAN TIDAK KENA PAJAK (PTKP)",
        compute="_compute_ptkp",
        store=True,
        readonly=True,
        compute_sudo=True,
    )

    @api.depends(
        "perhitungan_14",
        "perhitungan_15",
    )
    def _compute_pkp(self):
        """Compute ``perhitungan_16``, the taxable income (PKP).

        The taxable income is the annualized net income
        (``perhitungan_14``) minus PTKP (``perhitungan_15``), rounded
        down to the nearest thousand rupiah. Zero when PTKP is not
        exceeded.
        """
        for document in self:
            document.perhitungan_16 = 0.0
            if document.perhitungan_14 > document.perhitungan_15:
                document.perhitungan_16 = float(
                    int((document.perhitungan_14 - document.perhitungan_15) / 1000)
                    * 1000
                )

    perhitungan_16 = fields.Float(
        string="PENGHASILAN KENA PAJAK SETAHUN/DISETAHUNKAN",
        compute="_compute_pkp",
        store=True,
        readonly=True,
        compute_sudo=True,
    )

    @api.depends(
        "perhitungan_16",
    )
    def _compute_pph21(self):
        """Compute ``perhitungan_17``, the annual/annualized PPh 21.

        Delegates the progressive tax bracket calculation to
        ``wajib_pajak_id.compute_pph_21_2110001()``, passing the
        taxable income and related income components. Stays zero when
        the taxable income (``perhitungan_16``) is not positive.
        """
        for document in self:
            pph_21 = 0.0
            if document.perhitungan_16 > 0:
                tunj_lain = (
                    document.penghasilan_03
                    + document.penghasilan_04
                    + document.penghasilan_05
                    + document.penghasilan_06
                )
                perhitungan_pph = document.wajib_pajak_id.compute_pph_21_2110001(
                    1,
                    document.end_tax_period_id.date_end,
                    document.penghasilan_01,
                    document.penghasilan_02,
                    tunj_lain,
                    document.penghasilan_07,
                    document.pengurang_10,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    True,
                    not document.wajib_pajak_karyawan_asing,
                )
                pph_21 = perhitungan_pph["pph"]
            document.perhitungan_17 = pph_21

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

    @api.depends(
        "perhitungan_17",
        "perhitungan_18",
    )
    def _compute_hutang_pph(self):
        """Compute ``perhitungan_19``, the total PPh 21 payable.

        Adds the PPh 21 computed for the current period
        (``perhitungan_17``) to the amount already withheld in prior
        periods (``perhitungan_18``).
        """
        for document in self:
            document.perhitungan_19 = document.perhitungan_17 + document.perhitungan_18

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

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    def _get_localdict(self):
        """Build the local dict used to evaluate ``python_code`` config.

        Available locals: ``env`` (the current environment) and
        ``document`` (this record). The evaluated code is expected to
        set a ``result`` variable, which the caller reads back.

        :return: dict with keys ``env`` and ``document``
        """
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
        """Recompute ``penghasilan_01`` from the company's config code.

        Evaluates the ``python_code`` registered for this field on
        ``company_id`` (see ``res.company._get_python_1721_config``)
        and assigns its ``result`` to the field. Raises
        :class:`~odoo.exceptions.UserError` when the code fails.
        """
        self.penghasilan_01 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            python_code = self.company_id._get_python_1721_config("penghasilan_01")
            if python_code:
                result = 0.0
                try:
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    result = localdict["result"]
                except Exception as e:
                    msg_err = _(
                        """
                    Field: GAJI/PENSIUN ATAU THT/JHT
                    Massage Error: %s
                    """
                        % (e)
                    )
                    raise UserError(_("%s") % (msg_err))
                self.penghasilan_01 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_penghasilan_02(self):
        """Recompute ``penghasilan_02`` from the company's config code.

        Evaluates the ``python_code`` registered for this field on
        ``company_id`` (see ``res.company._get_python_1721_config``)
        and assigns its ``result`` to the field. Raises
        :class:`~odoo.exceptions.UserError` when the code fails.
        """
        self.penghasilan_02 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            python_code = self.company_id._get_python_1721_config("penghasilan_02")
            if python_code:
                result = 0.0
                try:
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    result = localdict["result"]
                except Exception as e:
                    msg_err = _(
                        """
                    Field: TUNJANGAN PPh
                    Massage Error: %s
                    """
                        % (e)
                    )
                    raise UserError(_("%s") % (msg_err))
                self.penghasilan_02 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_penghasilan_03(self):
        """Recompute ``penghasilan_03`` from the company's config code.

        Evaluates the ``python_code`` registered for this field on
        ``company_id`` (see ``res.company._get_python_1721_config``)
        and assigns its ``result`` to the field. Raises
        :class:`~odoo.exceptions.UserError` when the code fails.
        """
        self.penghasilan_03 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            python_code = self.company_id._get_python_1721_config("penghasilan_03")
            if python_code:
                result = 0.0
                try:
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    result = localdict["result"]
                except Exception as e:
                    msg_err = _(
                        """
                    Field: TUNJANGAN LAINNYA, UANG LEMBUR DAN SEBAGAINYA
                    Massage Error: %s
                    """
                        % (e)
                    )
                    raise UserError(_("%s") % (msg_err))
                self.penghasilan_03 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_penghasilan_04(self):
        """Recompute ``penghasilan_04`` from the company's config code.

        Evaluates the ``python_code`` registered for this field on
        ``company_id`` (see ``res.company._get_python_1721_config``)
        and assigns its ``result`` to the field. Raises
        :class:`~odoo.exceptions.UserError` when the code fails.
        """
        self.penghasilan_04 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            python_code = self.company_id._get_python_1721_config("penghasilan_04")
            if python_code:
                result = 0.0
                try:
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    result = localdict["result"]
                except Exception as e:
                    msg_err = _(
                        """
                    Field: HONORARIUM DAN IMBALAN LAIN SEJENISNYA
                    Massage Error: %s
                    """
                        % (e)
                    )
                    raise UserError(_("%s") % (msg_err))
                self.penghasilan_04 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_penghasilan_05(self):
        """Recompute ``penghasilan_05`` from the company's config code.

        Evaluates the ``python_code`` registered for this field on
        ``company_id`` (see ``res.company._get_python_1721_config``)
        and assigns its ``result`` to the field. Raises
        :class:`~odoo.exceptions.UserError` when the code fails.
        """
        self.penghasilan_05 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            python_code = self.company_id._get_python_1721_config("penghasilan_05")
            if python_code:
                result = 0.0
                try:
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    result = localdict["result"]
                except Exception as e:
                    msg_err = _(
                        """
                    Field: PREMI ASURANSI YANG DIBAYAR PEMBERI KERJA
                    Massage Error: %s
                    """
                        % (e)
                    )
                    raise UserError(_("%s") % (msg_err))
                self.penghasilan_05 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_penghasilan_06(self):
        """Recompute ``penghasilan_06`` from the company's config code.

        Evaluates the ``python_code`` registered for this field on
        ``company_id`` (see ``res.company._get_python_1721_config``)
        and assigns its ``result`` to the field. Raises
        :class:`~odoo.exceptions.UserError` when the code fails.
        """
        self.penghasilan_06 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            python_code = self.company_id._get_python_1721_config("penghasilan_06")
            if python_code:
                result = 0.0
                try:
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    result = localdict["result"]
                except Exception as e:
                    field = """PENERIMAAN DALAM BENTUK NATURA DAN KENIKMATAN
                            LAINNYA YANG DIKENAKAN PEMOTONGAN PPh PASAL 21"""
                    msg_err = _(
                        """
                    Field: %s
                    Massage Error: %s
                    """
                        % (field, e)
                    )
                    raise UserError(_("%s") % (msg_err))
                self.penghasilan_06 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_penghasilan_07(self):
        """Recompute ``penghasilan_07`` from the company's config code.

        Evaluates the ``python_code`` registered for this field on
        ``company_id`` (see ``res.company._get_python_1721_config``)
        and assigns its ``result`` to the field. Raises
        :class:`~odoo.exceptions.UserError` when the code fails.
        """
        self.penghasilan_07 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            python_code = self.company_id._get_python_1721_config("penghasilan_07")
            if python_code:
                result = 0.0
                try:
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    result = localdict["result"]
                except Exception as e:
                    msg_err = _(
                        """
                    Field: TANTIEM, BONUS, GRATIFIKASI, JASA PRODUKSI DAN THR
                    Massage Error: %s
                    """
                        % (e)
                    )
                    raise UserError(_("%s") % (msg_err))
                self.penghasilan_07 = result

    @api.depends(
        "penghasilan_01",
        "penghasilan_02",
        "penghasilan_03",
        "penghasilan_04",
        "penghasilan_05",
        "penghasilan_06",
        "penghasilan_07",
    )
    def _compute_penghasilan(self):
        """Compute ``penghasilan_08``, the total gross income.

        Sums ``penghasilan_01`` through ``penghasilan_07``.
        """
        for document in self:
            document.penghasilan_08 = 0.0
            document.penghasilan_08 = (
                document.penghasilan_01
                + document.penghasilan_02
                + document.penghasilan_03
                + document.penghasilan_04
                + document.penghasilan_05
                + document.penghasilan_06
                + document.penghasilan_07
            )

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_pengurang_10(self):
        """Recompute ``pengurang_10`` from the company's config code.

        Evaluates the ``python_code`` registered for this field on
        ``company_id`` (see ``res.company._get_python_1721_config``)
        and assigns its ``result`` to the field. Raises
        :class:`~odoo.exceptions.UserError` when the code fails.
        """
        self.pengurang_10 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            python_code = self.company_id._get_python_1721_config("pengurang_10")
            if python_code:
                result = 0.0
                try:
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    result = localdict["result"]
                except Exception as e:
                    msg_err = _(
                        """
                    Field: IURAN PENSIUN ATAU IURAN THT/JHT
                    Massage Error: %s
                    """
                        % (e)
                    )
                    raise UserError(_("%s") % (msg_err))
                self.pengurang_10 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_perhitungan_13(self):
        """Recompute ``perhitungan_13`` from the company's config code.

        Evaluates the ``python_code`` registered for this field on
        ``company_id`` (see ``res.company._get_python_1721_config``)
        and assigns its ``result`` to the field. Raises
        :class:`~odoo.exceptions.UserError` when the code fails.
        """
        self.perhitungan_13 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            python_code = self.company_id._get_python_1721_config("perhitungan_13")
            if python_code:
                result = 0.0
                try:
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    result = localdict["result"]
                except Exception as e:
                    msg_err = _(
                        """
                    Field: PENGHASILAN NETO MASA SEBELUMNYA
                    Massage Error: %s
                    """
                        % (e)
                    )
                    raise UserError(_("%s") % (msg_err))
                self.perhitungan_13 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_perhitungan_18(self):
        """Recompute ``perhitungan_18`` from the company's config code.

        Evaluates the ``python_code`` registered for this field on
        ``company_id`` (see ``res.company._get_python_1721_config``)
        and assigns its ``result`` to the field. Raises
        :class:`~odoo.exceptions.UserError` when the code fails.
        """
        self.perhitungan_18 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            python_code = self.company_id._get_python_1721_config("perhitungan_18")
            if python_code:
                result = 0.0
                try:
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    result = localdict["result"]
                except Exception as e:
                    msg_err = _(
                        """
                    Field: PPh PASAL 21 YANG TELAH DIPOTONG MASA SEBELUMNYA
                    Massage Error: %s
                    """
                        % (e)
                    )
                    raise UserError(_("%s") % (msg_err))
                self.perhitungan_18 = result

    @api.onchange(
        "company_id",
        "wajib_pajak_id",
        "start_tax_period_id",
        "end_tax_period_id",
    )
    def onchange_perhitungan_20(self):
        """Recompute ``perhitungan_20`` from the company's config code.

        Evaluates the ``python_code`` registered for this field on
        ``company_id`` (see ``res.company._get_python_1721_config``)
        and assigns its ``result`` to the field. Raises
        :class:`~odoo.exceptions.UserError` when the code fails.
        """
        self.perhitungan_20 = 0.0
        if self.company_id:
            localdict = self._get_localdict()
            python_code = self.company_id._get_python_1721_config("perhitungan_20")
            if python_code:
                result = 0.0
                try:
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    result = localdict["result"]
                except Exception as e:
                    msg_err = _(
                        """
                    Field: PPh PASAL 21 DAN PPh PASAL 26 YANG TELAH DIPOTONG DAN DILUNASI
                    Massage Error: %s
                    """
                        % (e)
                    )
                    raise UserError(_("%s") % (msg_err))
                self.perhitungan_20 = result

    @api.onchange(
        "tax_year_id",
    )
    def onchange_tax_year_id(self):
        self.start_tax_period_id = False
        self.end_tax_period_id = False
