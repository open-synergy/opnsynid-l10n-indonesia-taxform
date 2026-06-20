# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BuktiPotongPPhLineMixin(models.AbstractModel):
    _inherit = "l10n_id.bukti_potong_pph_line_mixin"

    coretax_tax_object_code = fields.Char(
        string="Coretax Tax Object Code",
        help=(
            "Tax object code used in the Coretax XML export "
            "(e.g. 23-100-01 for PPh 23 interest income)."
        ),
    )
