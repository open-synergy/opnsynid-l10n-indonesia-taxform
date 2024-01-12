# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class Pph21Rate(models.Model):
    _name = "l10n_id.pph_21_rate"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "PPh 21 Rate"
    _order = "date_start desc, id"

    date_start = fields.Date(
        string="Tanggal Mulai Berlaku",
        required=True,
    )
    line_ids = fields.One2many(
        string="PPh 21 Rate Detail",
        comodel_name="l10n_id.pph_21_rate_line",
        inverse_name="rate_id",
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
            strWarning = _("No PPh 21 rate configuration for %s" % dt)
            raise ValidationError(strWarning)
        return results[0]

    def compute_tax(self, penghasilan_kena_pajak):
        result = 0.0
        self.ensure_one()
        for line in range(0, len(self.line_ids)):
            if line < len(self.line_ids) - 1:
                next_line = self.line_ids[line + 1]
            else:
                next_line = False
            result += self.line_ids[line].compute_tax(penghasilan_kena_pajak, next_line)
        return result
