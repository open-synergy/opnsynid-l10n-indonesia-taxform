# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    lock_taxform = fields.Boolean(
        string="Lock Taxform",
        readonly=True,
        copy=False,
    )

    @api.depends(
        "type",
        "date_taxform",
    )
    @api.multi
    def _compute_allowed_nomor_seri_ids(self):
        obj_nsfp = self.env["l10n_id.nomor_seri_faktur_pajak"]
        for fp in self:
            result = []
            if fp.type == "out_invoice" and fp.date_taxform:
                criteria = [
                    ("taxform_year_id", "=", fp.taxform_year_id.id),
                    ("faktur_pajak_id", "=", False),
                ]
                result = obj_nsfp.search(criteria).ids
            fp.allowed_nomor_seri_ids = result

    allowed_nomor_seri_ids = fields.Many2many(
        string="Allowed Nomor Seri Faktur Pajak",
        comodel_name="l10n_id.nomor_seri_faktur_pajak",
        store=False,
        compute="_compute_allowed_nomor_seri_ids",
    )

    @api.depends(
        "date_taxform",
    )
    @api.multi
    def _compute_taxform_period(self):
        for fp in self:
            fp.taxform_period_id = False
            if fp.date_taxform:
                fp.taxform_period_id = (
                    self.env["l10n_id.tax_period"]._find_period(fp.date).id
                )

    @api.depends(
        "taxform_period_id",
    )
    @api.multi
    def _compute_taxform_year(self):
        for fp in self:
            fp.taxform_year_id = False
            if fp.taxform_period_id:
                fp.taxform_year_id = fp.taxform_period_id.year_id.id

    transaction_type_id = fields.Many2one(
        string="Transaction Type",
        comodel_name="l10n_id.faktur_pajak_transaction_type",
        copy=False,
    )
    fp_state = fields.Selection(
        string="Normal/Substitute?",
        selection=[
            ("0", "Normal"),
            ("1", "Substitute"),
        ],
        copy=False,
    )
    # Taxform Date and Period
    date_taxform = fields.Date(
        string="Document Date",
        copy=False,
    )
    taxform_period_id = fields.Many2one(
        string="Masa Pajak",
        comodel_name="l10n_id.tax_period",
        compute="_compute_taxform_period",
        store=True,
        copy=False,
    )
    taxform_year_id = fields.Many2one(
        string="Tahun Pajak",
        comodel_name="l10n_id.tax_year",
        compute="_compute_taxform_year",
        store=True,
        copy=False,
    )

    # Nomor Seri Faktur Pajak
    nomor_seri_id = fields.Many2one(
        string="Nomor Seri FP",
        comodel_name="l10n_id.nomor_seri_faktur_pajak",
        copy=False,
    )
    nomor_seri = fields.Char(
        string="Nomor Seri FP Manual",
        copy=False,
    )

    @api.depends(
        "transaction_type_id",
    )
    @api.multi
    def _compute_jenis_transaksi(self):
        for fp in self:
            result = "-"
            if fp.transaction_type_id:
                result = fp.transaction_type_id.code
            fp.enofa_jenis_transaksi = result

    # E-NOFA FIELDS
    enofa_jenis_transaksi = fields.Char(
        string="KD_JENIS_TRANSAKSI",
        compute="_compute_jenis_transaksi",
        store=False,
    )

    @api.depends(
        "transaction_type_id",
    )
    @api.multi
    def _compute_fg_pengganti(self):
        for fp in self:
            result = "-"
            if fp.fp_state:
                result = fp.fp_state
            fp.enofa_fg_pengganti = result

    enofa_fg_pengganti = fields.Char(
        string="FG_PENGGANTI",
        compute="_compute_fg_pengganti",
        store=False,
    )

    @api.depends(
        "type",
        "nomor_seri_id",
        "nomor_seri",
    )
    @api.multi
    def _compute_nomor_dokumen(self):
        for fp in self:
            result = "-"
            if fp.type == "out_invoice":
                if fp.nomor_seri_id:
                    result = fp.nomor_seri_id.name
            else:
                if fp.nomor_seri:
                    result = fp.nomor_ser
            fp.enofa_nomor_dokumen = result

    enofa_nomor_dokumen = fields.Char(
        string="NOMOR_DOKUMEN",
        compute="_compute_nomor_dokumen",
        store=False,
    )

    @api.depends(
        "taxform_period_id",
    )
    @api.multi
    def _compute_masa_pajak(self):
        for fp in self:
            result = "-"
            if fp.taxform_period_id:
                result = fp.taxform_period_id.code
            fp.enofa_masa_pajak = result

    enofa_masa_pajak = fields.Char(
        string="MASA_PAJAK",
        compute="_compute_masa_pajak",
        store=False,
    )

    @api.depends(
        "taxform_year_id",
    )
    @api.multi
    def _compute_tahun_pajak(self):
        for fp in self:
            result = "-"
            if fp.taxform_year_id:
                result = fp.taxform_year_id.code
            fp.enofa_tahun_pajak = result

    enofa_tahun_pajak = fields.Char(
        string="TAHUN_PAJAK",
        compute="_compute_tahun_pajak",
        store=False,
    )

    @api.depends(
        "date_taxform",
    )
    @api.multi
    def _compute_tanggal_dokumen(self):
        for fp in self:
            fp.enofa_tanggal_dokumen = "-"
            if fp.date_taxform:
                fp.enofa_tanggal_dokumen = datetime.strptime(
                    fp.date_taxform, "%Y-%m-%d"
                ).strftime("%d/%m/%Y")

    enofa_tanggal_dokumen = fields.Char(
        string="TANGGAL_DOKUMEN",
        compute="_compute_tanggal_dokumen",
        store=False,
    )

    @api.depends(
        "type",
        "partner_id",
        "company_id",
    )
    @api.multi
    def _compute_npwp(self):
        for fp in self:
            fp.enofa_npwp = "000000000000000"
            if fp.type in ["out_invoice", "out_refund"]:
                if fp.company_id.partner_id.vat:
                    npwp = fp.company_id.partner_id.vat
                    fp.enofa_npwp = ""
                    for s in re.findall(r"\d+", npwp):
                        fp.enofa_npwp += s
            else:
                if fp.partner_id.commercial_partner_id.vat:
                    npwp = fp.partner_id.commercial_partner_id.vat
                    fp.enofa_npwp = ""
                    for s in re.findall(r"\d+", npwp):
                        fp.enofa_npwp += s

    enofa_npwp = fields.Char(
        string="NPWP",
        compute="_compute_npwp",
        store=False,
    )

    @api.depends(
        "type",
        "partner_id",
        "company_id",
    )
    @api.multi
    def _compute_nama(self):
        for fp in self:
            fp.enofa_nama = "-"
            if fp.type in ["out_invoice", "out_refund"]:
                fp.enofa_nama = fp.company_id.name
            else:
                fp.enofa_nama = fp.partner_id.commercial_partner_id.name

    enofa_nama = fields.Char(
        string="NAMA",
        compute="_compute_nama",
        store=False,
    )

    @api.depends(
        "type",
        "partner_id",
        "company_id",
    )
    @api.multi
    def _compute_alamat_lengkap(self):
        for fp in self:
            fp.enofa_alamat_lengkap = "-"
            if fp.type in ["out_invoice", "out_refund"]:
                fp.enofa_alamat_lengkap = fp.company_id.partner_id.enofa_address
            else:
                fp.enofa_alamat_lengkap = (
                    fp.partner_id.commercial_partner_id.enofa_address
                )

    enofa_alamat_lengkap = fields.Char(
        string="ALAMAT_LENGKAP",
        compute="_compute_alamat_lengkap",
        store=False,
    )

    @api.depends(
        "tax_line_ids",
        "tax_line_ids.tax_id",
        "tax_line_ids.amount",
        "tax_line_ids.amount_rounding",
    )
    @api.multi
    def _compute_jumlah_dpp(self):
        for fp in self:
            fp.enofa_jumlah_dpp = fp.amount_untaxed

    @api.depends(
        "tax_line_ids",
        "tax_line_ids.tax_id",
        "tax_line_ids.amount",
        "tax_line_ids.amount_rounding",
    )
    @api.multi
    def _compute_jumlah_ppn(self):
        for fp in self:
            fp.enofa_jumlah_ppn = fp.amount_tax

    @api.depends(
        "tax_line_ids",
        "tax_line_ids.tax_id",
        "tax_line_ids.amount",
        "tax_line_ids.amount_rounding",
    )
    @api.multi
    def _compute_jumlah_ppnbm(self):
        for fp in self:
            fp.enofa_jumlah_ppnbm = 0.0

    enofa_jumlah_dpp = fields.Integer(
        string="JUMLAH_DPP",
        compute="_compute_jumlah_dpp",
        store=False,
    )
    enofa_jumlah_ppn = fields.Integer(
        string="JUMLAH_PPN",
        compute="_compute_jumlah_ppn",
        store=False,
    )
    enofa_jumlah_ppnbm = fields.Integer(
        string="JUMLAH_DPP",
        compute="_compute_jumlah_ppnbm",
        store=False,
    )

    @api.multi
    def action_lock_taxform(self):
        for doc in self:
            doc._lock_taxform()

    @api.multi
    def _lock_taxform(self):
        self.ensure_one()
        self.write(self._prepare_lock_taxform())
        if self.type == "out_invoice":
            self.nomor_seri_id.mark_used(self)

    @api.multi
    def _prepare_lock_taxform(self):
        self.ensure_one()
        return {
            "lock_taxform": True,
        }

    @api.multi
    def action_unlock_taxform(self):
        for doc in self:
            doc._unlock_taxform()

    @api.multi
    def _unlock_taxform(self):
        self.ensure_one()
        self.write(self._prepare_unlock_taxform())
        if self.type == "out_invoice":
            self.nomor_seri_id.mark_unused()

    @api.multi
    def _prepare_unlock_taxform(self):
        self.ensure_one()
        return {
            "lock_taxform": False,
        }

    @api.constrains(
        "lock_taxform",
        "nomor_seri_id",
        "nomor_seri",
    )
    def _check_lock_taxform(self):
        error_msg = _("Please fill taxform number")
        for doc in self:
            if doc.type == "out_invoice" and not doc.nomor_seri_id and doc.lock_taxform:
                raise UserError(error_msg)
            elif (
                doc.type != "out_invoice" and not doc.nomor_seri_id and doc.lock_taxform
            ):
                raise UserError(error_msg)
