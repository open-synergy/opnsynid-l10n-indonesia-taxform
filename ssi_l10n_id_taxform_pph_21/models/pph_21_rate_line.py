# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models


class Pph21RateLine(models.Model):
    _name = "l10n_id.pph_21_rate_line"
    _description = "PPh 21 Rate Line"
    _order = "min_income asc"

    rate_id = fields.Many2one(
        string="PPh 21 Rate",
        comodel_name="l10n_id.pph_21_rate",
        ondelete="cascade",
    )
    min_income = fields.Float(
        string="Min. Income",
        required=True,
    )
    pph_rate = fields.Float(
        string="PPh 21 Rate",
    )

    def compute_tax(self, penghasilan_kena_pajak, next_line):
        self.ensure_one()
        result = 0.0
        pph_rate = self.pph_rate / 100.00
        if penghasilan_kena_pajak > self.min_income:
            if not next_line:
                result = pph_rate * (penghasilan_kena_pajak - self.min_income)
            else:
                if penghasilan_kena_pajak >= next_line.min_income:
                    result = pph_rate * (next_line.min_income - self.min_income)
                else:
                    result = pph_rate * (penghasilan_kena_pajak - self.min_income)
        return result
