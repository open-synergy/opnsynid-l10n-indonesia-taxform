# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class L10nIdBuktiPotongPphF113310Out(models.Model):
    """
    Extend Bukti Potong PPh f.1.1.33.10 Keluaran with single operating
    unit support.

    Adds the ``operating_unit_id`` field (via the single operating
    unit mixin) so each record can be scoped to one operating unit.
    This document does not generate any other document, so no
    operating unit propagation is required.
    """

    _name = "l10n_id.bukti_potong_pph_f113310_out"
    _inherit = [
        "l10n_id.bukti_potong_pph_f113310_out",
        "mixin.single_operating_unit",
    ]
