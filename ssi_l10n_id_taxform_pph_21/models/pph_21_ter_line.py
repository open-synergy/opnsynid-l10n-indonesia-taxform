# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models


class Pph21TerLine(models.Model):
    _name = "l10n_id.pph_21_ter_line"
    _description = "PPh 21 Tarif Efektif Rata Rata Lines"

    ter_id = fields.Many2one(
        string="#TER",
        comodel_name="l10n_id.pph_21_ter",
        ondelete="cascade",
    )
    name = fields.Char(
        string="Name",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    ptkp_category_ids = fields.Many2many(
        string="PTKP Categories",
        comodel_name="l10n_id.ptkp_category",
        relation="pph_21_ter_2_ptkp_categ_rel",
        column1="ter_id",
        column2="category_id",
        required=True,
    )
    line_ids = fields.One2many(
        string="Details",
        comodel_name="l10n_id.pph_21_ter_line_categ",
        inverse_name="ter_line_id",
    )

    def compute_tax(self, bruto):
        self.ensure_one()
        result = {
            "ter": self.name,
            "rate": 0.00,
            "pph": 0.00,
        }
        for line in range(0, len(self.line_ids) + 1):
            if line < len(self.line_ids):
                if bruto >= self.line_ids[line].min_income:
                    continue
                else:
                    result["rate"] = self.line_ids[line - 1].pph_rate
                    result["pph"] = (self.line_ids[line - 1].pph_rate / 100.00) * bruto
                    break
            else:
                result["rate"] = self.line_ids[line - 1].pph_rate
                result["pph"] = (self.line_ids[line - 1].pph_rate / 100.00) * bruto
        return result
