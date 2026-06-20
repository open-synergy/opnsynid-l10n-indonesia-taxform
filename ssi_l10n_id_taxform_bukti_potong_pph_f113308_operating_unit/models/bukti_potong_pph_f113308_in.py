# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class BuktiPotongPPhf113308In(models.Model):
    _name = "l10n_id.bukti_potong_pph_f113308_in"
    _inherit = [
        "l10n_id.bukti_potong_pph_f113308_in",
        "mixin.single_operating_unit",
    ]
