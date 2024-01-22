# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models


class Pph21TerLineCateg(models.Model):
    _name = "l10n_id.pph_21_ter_line_categ"
    _description = "PPh 21 Tarif Efektif Rata Rata Lines Categ"
    _order = "min_income asc"

    ter_line_id = fields.Many2one(
        string="#LINE TER",
        comodel_name="l10n_id.pph_21_ter_line",
        ondelete="cascade",
    )
    min_income = fields.Float(
        string="Min. Income",
        required=True,
    )
    pph_rate = fields.Float(
        string="PPh 21 Rate",
    )
