# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class L10nIdTaxformJenisDokumenReferensi(models.Model):
    """
    Represents an Indonesian reference document type (Jenis Dokumen
    Referensi) master record. Each record holds the code and
    description of a source document type (mis. invoice, contract)
    a BP21 withholding line can cite (the ``Document`` element of
    the Coretax withholding XML).
    """

    _name = "l10n_id.taxform_jenis_dokumen_referensi"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Taxform Jenis Dokumen Referensi"

    @api.model
    def _default_company_id(self):
        """Return the default company for a new reference document
        type record.

        :return: ID of the current user's company
        """
        return self.env.user.company_id.id

    code = fields.Char(
        string="Jenis Dokumen Referensi",
        required=True,
        translate=True,
    )
    name = fields.Text(
        string="Description",
        required=True,
        translate=True,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
        ondelete="restrict",
        readonly=True,
    )
