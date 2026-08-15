# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class L10nIdBuktiPotongPph1721A1(models.Model):
    """
    Extends Tax Form 1721 A1 with single operating unit support.

    Restricts each document to one operating unit
    (``operating_unit_id``, from ``mixin.single_operating_unit``),
    defaulting to the creating user's default operating unit. This
    module does not generate any other document, so no operating
    unit propagation is required.
    """

    _name = "l10n_id.bukti_potong_pph_1721_a1"
    _inherit = [
        "l10n_id.bukti_potong_pph_1721_a1",
        "mixin.single_operating_unit",
    ]
