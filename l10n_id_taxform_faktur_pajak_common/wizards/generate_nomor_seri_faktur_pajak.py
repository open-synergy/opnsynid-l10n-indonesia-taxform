# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from openerp import api, fields, models


class GenerateNomorSeriFakturPajak(models.TransientModel):
    _name = "l10n_id.generate_nomor_seri_faktur_pajak"
    _description = "Generate Nomor Seri Faktur Pajak"

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
    taxform_year_id = fields.Many2one(
        string="Tahun Pajak",
        comodel_name="l10n_id.tax_year",
        required=True,
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
        required=True,
    )
    quantity = fields.Integer(
        string="Number of.",
        required=True,
        default=1,
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
    def generate_nomor_seri(self):
        self.ensure_one()
        for _qty in range(1, self.quantity + 1):
            name = self.sequence_id._next()
            data = {
                "name": name,
                "company_id": self.company_id.id,
                "branch_id": self.branch_id.id,
                "taxform_year_id": self.taxform_year_id.id,
            }
            self.env["l10n_id.nomor_seri_faktur_pajak"].create(data)
