# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class BuktiPotongPPhf113301Out(models.Model):
    _name = "l10n_id.bukti_potong_pph_f113301_out"
    _inherit = [
        "l10n_id.bukti_potong_pph_f113301_out",
        "mixin.work_object",
    ]

    _work_log_create_page = True
