# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    """
    Adds Form 1721 A1 field-computation configuration to the company.
    Each company can register a set of per-field Python rules used to
    auto-fill onchange-computed fields on
    ``l10n_id.bukti_potong_pph_1721_a1``.
    """

    _inherit = "res.company"

    pph_1721a1_config = fields.One2many(
        string="Form 1721 A1 Config",
        comodel_name="l10n_id.bukti_potong_pph_1721_a1_config",
        inverse_name="company_id",
    )

    def _get_python_1721_config(self, field):
        """Return the configured Python code for a Form 1721 A1 field.

        Looks up ``pph_1721a1_config`` for an entry whose ``field_id``
        matches ``field`` and returns its ``python_code``. Used by the
        ``onchange_*`` methods of ``l10n_id.bukti_potong_pph_1721_a1``.

        :param field: technical name of the target field
        :return: the configured Python code, or ``False`` if none
        """
        self.ensure_one()
        result = False
        if self.pph_1721a1_config:
            config_id = self.pph_1721a1_config.filtered(
                lambda x: x.field_id.name == field
            )
            if config_id:
                result = config_id.python_code
        return result
