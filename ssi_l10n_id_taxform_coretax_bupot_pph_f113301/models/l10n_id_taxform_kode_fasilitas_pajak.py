# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class L10nIdTaxformKodeFasilitasPajak(models.Model):
    """
    Represents an Indonesian tax facility code (Kode Fasilitas Pajak)
    master record. Each record holds the code and description of a
    DGT tax exemption/facility used on BP21 withholding lines (the
    ``TaxCertificate`` element of the Coretax withholding XML).
    """

    _name = "l10n_id.taxform_kode_fasilitas_pajak"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Taxform Kode Fasilitas Pajak"

    @api.model
    def _default_company_id(self):
        """Return the default company for a new tax facility record.

        :return: ID of the current user's company
        """
        return self.env.user.company_id.id

    code = fields.Char(
        string="Kode Fasilitas Pajak",
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
