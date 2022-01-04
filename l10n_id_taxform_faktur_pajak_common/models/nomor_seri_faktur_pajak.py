# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class NomorSeriFakturPajak(models.Model):
    _name = "l10n_id.nomor_seri_faktur_pajak"
    _description = "Nomor Seri Faktur Pajak"

    name = fields.Char(
        string="Nomor Seri",
        readonly=False,
        required=True,
    )
    faktur_pajak_id = fields.Many2one(
        comodel_name="account.invoice",
        string="# Invoice",
        readonly=True,
        ondelete="restrict",
        required=False,
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
    def mark_used(self, fp):
        self.ensure_one()
        self.faktur_pajak_id = fp

    @api.multi
    def mark_unused(self):
        self.ensure_one()
        self.faktur_pajak_id = False
