# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class BuktiPotongPPh1721A1(models.Model):
    _name = "l10n_id.bukti_potong_pph_1721_a1"
    _inherit = [
        "l10n_id.bukti_potong_pph_1721_a1",
        "mixin.single_operating_unit",
    ]
