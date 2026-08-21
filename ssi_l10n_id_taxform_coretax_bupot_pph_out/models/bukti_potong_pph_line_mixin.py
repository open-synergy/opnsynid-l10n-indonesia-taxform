# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BuktiPotongPPhLineMixin(models.AbstractModel):
    """Adds the Coretax tax object code to a Bukti Potong PPh line.

    ``coretax_tax_object_code`` tags each withholding line with the
    tax object code required by the DGT Coretax XML schema, so the
    export built in ``BuktiPotongPPhMixin`` can populate the
    ``TaxObjectCode`` element of every ``MmWithholding`` entry.
    """

    _inherit = "l10n_id.bukti_potong_pph_line_mixin"

    coretax_tax_object_code = fields.Char(
        string="Coretax Tax Object Code",
        help=(
            "Tax object code used in the Coretax XML export "
            "(e.g. 23-100-01 for PPh 23 interest income)."
        ),
    )
