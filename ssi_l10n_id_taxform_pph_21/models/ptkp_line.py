# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models
from odoo.tools.translate import _


class PtkpLine(models.Model):
    _name = "l10n_id.ptkp_line"
    _description = "PTKP Line"

    ptkp_id = fields.Many2one(
        string="PTKP",
        comodel_name="l10n_id.ptkp",
        ondelete="cascade",
    )
    ptkp_category_id = fields.Many2one(
        string="PTKP Category",
        comodel_name="l10n_id.ptkp_category",
        required=True,
    )
    ptkp_rate = fields.Float(
        string="Tarif PTKP",
        required=True,
    )

    _sql_constraints = [
        (
            "pktp_category_use_only_once",
            "unique(ptkp_id, ptkp_category_id)",
            _("PTKP category can only be used once on each PTKP"),
        )
    ]
