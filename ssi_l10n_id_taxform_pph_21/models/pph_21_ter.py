# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class Pph21Ter(models.Model):
    _name = "l10n_id.pph_21_ter"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "PPh 21 Tarif Efektif Rata Rata"

    date_start = fields.Date(
        string="Tanggal Mulai Berlaku",
        required=True,
    )
    line_ids = fields.One2many(
        string="Details",
        comodel_name="l10n_id.pph_21_ter_line",
        inverse_name="ter_id",
    )

    @api.model
    def find(self, dt=None):
        if not dt:
            dt = datetime.now().strftime("%Y-%m-%d")
        criteria = [
            ("date_start", "<=", dt),
        ]
        results = self.search(criteria, limit=1)
        if not results:
            strWarning = _("No PPh 21 TER configuration for %s" % dt)
            raise ValidationError(strWarning)
        return results[0]

    def compute_tax(self, bruto, ptkp_category_ids):
        self.ensure_one()
        criteria = [
            ("ptkp_category_ids", "in", ptkp_category_ids),
        ]
        lines = self.line_ids.search(criteria)
        if not lines:
            strWarning = _("No PPh 21 Details TER configuration")
            raise ValidationError(strWarning)
        return lines.compute_tax(bruto)
