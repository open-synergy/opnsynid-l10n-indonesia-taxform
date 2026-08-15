# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class L10nIdBuktiPotongPphF113302Out(models.Model):
    """
    Enables work hour logging on f.1.1.33.02 (Out) withholding slips.

    Adds the ``mixin.work_object`` capability to
    ``l10n_id.bukti_potong_pph_f113302_out`` so users can record work
    log entries (``hr.work_log``) against a withholding slip, track
    estimated vs. realized work, and link entries to an analytic
    account.
    """

    _name = "l10n_id.bukti_potong_pph_f113302_out"
    _inherit = [
        "l10n_id.bukti_potong_pph_f113302_out",
        "mixin.work_object",
    ]

    _work_log_create_page = True
