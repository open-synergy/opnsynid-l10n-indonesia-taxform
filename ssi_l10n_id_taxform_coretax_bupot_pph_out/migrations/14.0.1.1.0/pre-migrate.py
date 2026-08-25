# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.0.0 -> 14.0.1.1.0
#
# Changes: ``coretax_tax_object_code`` on ``l10n_id.bukti_potong_pph_
#          line_mixin`` changes from Char to Many2one (comodel
#          ``l10n_id.taxform_objek_pajak``). The mixin is abstract, so
#          the column lives on every concrete bukti potong pph line
#          table that inherits it; this instance may only have some
#          of them installed. Rename the free-text column aside on
#          whichever of those tables actually exist, before Odoo
#          creates the new integer FK column under the same name, so
#          post-migrate can map the old codes to the new master
#          records.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

# Every concrete model known to inherit
# ``l10n_id.bukti_potong_pph_line_mixin`` at the time of this
# migration (both directions, all bukti potong pph form types).
CONCRETE_LINE_TABLES = [
    "l10n_id_bukti_potong_pph_f113301_out_line",
    "l10n_id_bukti_potong_pph_f113302_out_line",
    "l10n_id_bukti_potong_pph_f113304_in_line",
    "l10n_id_bukti_potong_pph_f113304_out_line",
    "l10n_id_bukti_potong_pph_f113306_in_line",
    "l10n_id_bukti_potong_pph_f113306_out_line",
    "l10n_id_bukti_potong_pph_f113308_in_line",
    "l10n_id_bukti_potong_pph_f113308_out_line",
    "l10n_id_bukti_potong_pph_f113310_in_line",
    "l10n_id_bukti_potong_pph_f113310_out_line",
]

OLD_COLUMN = "coretax_tax_object_code"
OLD_COLUMN_BACKUP = "coretax_tax_object_code_old_char"


@openupgrade.migrate()
def migrate(env, version):
    """Preserve the free-text tax object code on every installed line
    table before the field becomes a Many2one.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; renames ``coretax_tax_object_code`` columns
    """
    cr = env.cr
    for table in CONCRETE_LINE_TABLES:
        if not openupgrade.table_exists(cr, table):
            _logger.info("Skip %s: table does not exist here.", table)
            continue
        if not openupgrade.column_exists(cr, table, OLD_COLUMN):
            _logger.info("Skip %s: column %s does not exist here.", table, OLD_COLUMN)
            continue
        openupgrade.rename_columns(cr, {table: [(OLD_COLUMN, OLD_COLUMN_BACKUP)]})
        _logger.info("Renamed %s.%s to %s.", table, OLD_COLUMN, OLD_COLUMN_BACKUP)
