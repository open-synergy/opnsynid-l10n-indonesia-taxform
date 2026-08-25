# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.0.0 -> 14.0.1.1.0
#
# Changes: map the free-text tax object codes preserved by
#          pre-migrate.py (``coretax_tax_object_code_old_char``) to
#          the matching ``l10n_id.taxform_objek_pajak`` master record
#          on every installed bukti potong pph line table, now that
#          Odoo has created the new Many2one column under the
#          original name. Codes that do not match any master record
#          are left unmapped (logged) rather than guessed at.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

# Keep in sync with pre-migrate.py.
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

NEW_COLUMN = "coretax_tax_object_code"
OLD_COLUMN_BACKUP = "coretax_tax_object_code_old_char"
OBJEK_PAJAK_TABLE = "l10n_id_taxform_objek_pajak"


@openupgrade.migrate()
def migrate(env, version):
    """Map the preserved free-text tax object codes to the matching
    ``l10n_id.taxform_objek_pajak`` master record.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates ``coretax_tax_object_code`` on every
        installed bukti potong pph line table
    """
    cr = env.cr
    for table in CONCRETE_LINE_TABLES:
        if not openupgrade.column_exists(cr, table, OLD_COLUMN_BACKUP):
            _logger.info(
                "Skip %s: %s not found (pre-migrate did not touch it " "here).",
                table,
                OLD_COLUMN_BACKUP,
            )
            continue

        openupgrade.logged_query(
            cr,
            """
            UPDATE {table} AS line
            SET {new_column} = objek_pajak.id
            FROM {objek_pajak_table} AS objek_pajak
            WHERE line.{old_column} = objek_pajak.code
              AND line.{old_column} IS NOT NULL
            """.format(
                table=table,
                new_column=NEW_COLUMN,
                objek_pajak_table=OBJEK_PAJAK_TABLE,
                old_column=OLD_COLUMN_BACKUP,
            ),
        )
        _logger.info("Mapped %s.%s: %s row(s).", table, NEW_COLUMN, cr.rowcount)

        openupgrade.logged_query(
            cr,
            """
            SELECT COUNT(*) FROM {table}
            WHERE {old_column} IS NOT NULL AND {new_column} IS NULL
            """.format(
                table=table,
                old_column=OLD_COLUMN_BACKUP,
                new_column=NEW_COLUMN,
            ),
        )
        unmapped = cr.fetchone()[0]
        if unmapped:
            _logger.warning(
                "%s: %s row(s) had a coretax_tax_object_code with no "
                "matching l10n_id.taxform_objek_pajak master record "
                "(kept in %s for manual review).",
                table,
                unmapped,
                OLD_COLUMN_BACKUP,
            )
