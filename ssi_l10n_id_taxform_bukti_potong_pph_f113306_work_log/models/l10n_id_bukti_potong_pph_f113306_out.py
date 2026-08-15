# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class L10nIdBuktiPotongPphF113306Out(models.Model):
    """Add Work Log tracking to the PPh 23 outgoing withholding slip.

    Glue module: enables the Work Log tab (``mixin.work_object``) on
    ``l10n_id.bukti_potong_pph_f113306_out`` so hours spent processing
    this document can be recorded against ``hr.work_log``.
    """

    _name = "l10n_id.bukti_potong_pph_f113306_out"
    _inherit = [
        "l10n_id.bukti_potong_pph_f113306_out",
        "mixin.work_object",
    ]

    _work_log_create_page = True
