# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from openerp import api, fields, models


class NomorSeriFakturPajak(models.Model):
    _name = "l10n_id.nomor_seri_faktur_pajak"
    _description = "Nomor Seri Faktur Pajak"
    _order = "taxform_year_id, name"

    name = fields.Char(
        string="Nomor Seri",
        readonly=False,
        required=True,
    )
    invoice_ids = fields.One2many(
        sting="Invoices",
        comodel_name="account.invoice",
        inverse_name="nomor_seri_id",
        readonly=True,
    )
    lock_nomor_seri = fields.Boolean(
        string="Lock Nomor Seri",
        readonly=True,
        default=False,
        copy=False,
    )
    taxform_year_id = fields.Many2one(
        string="Tahun Pajak",
        comodel_name="l10n_id.tax_year",
        required=True,
    )

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    branch_id = fields.Many2one(
        string="Branch",
        comodel_name="res.partner",
        ondelete="restrict",
        required=True,
    )

    @api.onchange("company_id")
    def onchange_company(self):
        # TODO: Refactoring
        result = {}
        if self.company_id:
            if self.branch_id:
                if self.branch_id.commercial_partner_id != self.company_id.partner_id:
                    self.branch_id = False
            else:
                self.branch_id = self.company_id.partner_id
        else:
            self.branch_id = False
        result["domain"] = {
            "branch_id": [
                ("is_company", "=", True),
                ("id", "child_of", self.company_id.partner_id.id),
            ],
        }
        return result

    @api.multi
    def action_lock_nomor_seri(self):
        for doc in self:
            doc._lock_nomor_seri()

    @api.multi
    def _lock_nomor_seri(self):
        self.ensure_one()
        obj_account_invoice = self.env["account.invoice"]
        criteria = self._prepare_criteria_invoice()
        invoice_ids = obj_account_invoice.search(criteria)
        if invoice_ids:
            for invoice in invoice_ids:
                invoice._lock_taxform()
            self.write(self._prepare_lock_nomor_seri())

    @api.multi
    def _prepare_criteria_invoice(self):
        self.ensure_one()
        criteria = [("nomor_seri_id", "=", self.id)]
        return criteria

    @api.multi
    def _prepare_lock_nomor_seri(self):
        self.ensure_one()
        return {
            "lock_nomor_seri": True,
        }

    @api.multi
    def action_unlock_nomor_seri(self):
        for doc in self:
            doc._unlock_nomor_seri()

    @api.multi
    def _unlock_nomor_seri(self):
        self.ensure_one()
        obj_account_invoice = self.env["account.invoice"]
        criteria = self._prepare_criteria_invoice()
        invoice_ids = obj_account_invoice.search(criteria)
        if invoice_ids:
            for invoice in invoice_ids:
                invoice._unlock_taxform()
            self.write(self._prepare_unlock_nomor_seri())

    @api.multi
    def _prepare_unlock_nomor_seri(self):
        self.ensure_one()
        return {
            "lock_nomor_seri": False,
        }
