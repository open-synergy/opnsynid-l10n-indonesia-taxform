# Copyright 2017 Andhitia Rama
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.depends(
        "street",
        "street2",
        "state_id",
        "zip",
    )
    @api.multi
    def _compute_enofa_address(self):
        addrs = "%s %s.%s %s"
        for partner in self:
            partner.enofa_address = addrs % (
                partner.street,
                partner.street2 or "",
                partner.state_id and partner.state_id.name or "-",
                partner.zip or "-",
            )

    enofa_address = fields.Char(
        string="Address for E-Nofa",
        compute="_compute_enofa_address",
        store=False,
    )
    type = fields.Selection(selection_add=[("tax", "Tax Address")])
