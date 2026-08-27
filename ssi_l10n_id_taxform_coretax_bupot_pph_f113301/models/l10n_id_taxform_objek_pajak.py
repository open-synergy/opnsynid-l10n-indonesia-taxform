# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class L10nIdTaxformObjekPajak(models.Model):
    """
    Adds the Coretax DPP/tariff-regime data BP21 needs to the shared
    tax object code master: the ``deemed`` factor used to derive the
    DPP from gross income, and the tariff regime (TER/PS17/Harian/
    Pesangon/Pensiun) used to pick how the withholding rate is
    computed.
    """

    _name = "l10n_id.taxform_objek_pajak"
    _inherit = [
        "l10n_id.taxform_objek_pajak",
    ]

    deemed = fields.Float(
        string="Deemed",
        default=1.0,
        help=(
            "Fraction of gross income used as the DPP (Dasar Pengenaan "
            "Pajak) for this tax object, e.g. 0.5 for 50% deemed profit. "
            "Leave at 1.0 (100%) when the full gross income is the DPP."
        ),
    )
    tariff_type = fields.Selection(
        string="Jenis Tarif",
        selection=[
            ("ter", "TER (Tarif Efektif Rata-Rata)"),
            ("ps17", "PS17 (Pasal 17)"),
            ("harian", "Harian"),
            ("pesangon", "Pesangon"),
            ("pensiun", "Pensiun"),
            ("final_flat", "Final (Tarif Tetap per Kode Objek Pajak)"),
        ],
        help=(
            "DGT tariff regime used to determine the withholding rate "
            "for withholding lines using this tax object."
        ),
    )
    fixed_rate = fields.Float(
        string="Tarif Tetap",
        default=0.0,
        help=(
            "Fixed withholding rate applied when Tariff Type is Final "
            "(Tarif Tetap per Kode Objek Pajak), as a fraction (e.g. "
            "0.05 for 5%). Ignored for every other tariff type."
        ),
    )
