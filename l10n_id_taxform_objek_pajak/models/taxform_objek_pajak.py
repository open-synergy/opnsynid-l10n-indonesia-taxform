# Copyright 2021 Simetri Sinergi Indonesia, OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class TaxformObjekPajak(models.Model):
    _name = "l10n_id.taxform_objek_pajak"
    _inherit = ["mail.thread"]
    _description = "Taxform Objek Pajak"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    name = fields.Char(
        string="Kode Objek Pajak",
        required=True,
        translate=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    description = fields.Text(
        string="Description",
        translate=True,
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
