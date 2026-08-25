# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError


class ReportSsiL10nIdTaxformCoretaxBupotPphF113301Xml(models.AbstractModel):
    """Render the Coretax XML for an outgoing BP21 (f.1.1.33.01) slip.

    Backs the ``qweb-xml`` report bound to
    ``l10n_id.bukti_potong_pph_f113301_out`` (visible in the form's
    Print dropdown) that reuses
    ``_prepare_coretax_bupot_pph_out_values`` — the same values
    already used by the generic Export Coretax XML button.
    """

    _name = "report.ssi_l10n_id_taxform_coretax_bupot_pph_f113301.xml"
    _inherit = [
        "report.report_xml.abstract",
    ]
    _description = "Coretax BP21 (f.1.1.33.01) Withholding XML Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        """Build the rendering context for the Coretax XML template.

        :param docids: ids of the ``l10n_id.bukti_potong_pph_f113301_
            out`` record being printed (exactly one — Print does not
            support bulk XML export for this report)
        :param data: unused, kept for the ``ir.actions.report``
            signature
        :raises UserError: when the document is not yet Done, or when
            required Coretax data is missing (see
            ``_prepare_coretax_bupot_pph_out_values``)
        :return: dict of rendering values for the ``coretax_xml``
            template
        """
        bukpot = self.env["l10n_id.bukti_potong_pph_f113301_out"].browse(docids)
        bukpot.ensure_one()
        if bukpot.state != "done":
            error_message = _(
                """
Context: Print Coretax BP21 (f.1.1.33.01) XML
Database ID: %s
Problem: This document is not yet Done (current status: %s)
Solution: Confirm and approve the document before printing the
Coretax XML
"""
                % (bukpot.id, bukpot.state)
            )
            raise UserError(error_message)
        return bukpot._prepare_coretax_bupot_pph_out_values()
