# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class Ptkp(models.Model):
    _name = "l10n_id.ptkp"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Tarif PTKP"
    _order = "date_start desc, id"

    date_start = fields.Date(
        string="Tanggal Mulai Berlaku",
        required=True,
    )
    line_ids = fields.One2many(
        string="Detail Tarif",
        comodel_name="l10n_id.ptkp_line",
        inverse_name="ptkp_id",
    )

    _sql_constraints = [
        ("date_start_unique", "unique(date_start)", _("Date start has to be unique"))
    ]

    @api.model
    def find(self, dt=None):
        if not dt:
            dt = datetime.now().strftime("%Y-%m-%d")
        criteria = [("date_start", "<=", dt)]
        results = self.search(criteria, limit=1)
        if not results:
            strWarning = _("No PTKP rate configuration for %s" % dt)
            raise ValidationError(strWarning)
        return results[0]

    def get_rate(self, ptkp_category):
        self.ensure_one()
        lines = self.line_ids.filtered(
            lambda r: r.ptkp_category_id.id == ptkp_category.id
        )
        if not lines:
            raise ValidationError(_("Wes"))
        return lines[0].ptkp_rate
