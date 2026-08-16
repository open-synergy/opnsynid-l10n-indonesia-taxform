# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ReportSsiL10nIdTaxformCoretaxBupot21PayslipBatchBpmp(models.AbstractModel):
    """Render the Coretax BPMP XML for a payslip batch.

    Backs the ``qweb-xml`` report bound to ``hr.payslip_batch`` that the
    Export Coretax PPh 21 XML wizard triggers.
    """

    _name = "report.ssi_l10n_id_taxform_coretax_bupot_21_payslip_batch.bpmp"
    _description = "Coretax PPh 21 Withholding XML Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        """Build the QWeb rendering context for the Coretax BPMP XML.

        :param docids: ``hr.payslip_batch`` ids being rendered
        :param data: dict with ``bruto_rule_id`` and ``pph_rule_id``, the
            salary rules selected on the export wizard
        :return: the dict built by
            ``hr.payslip_batch._prepare_coretax_bupot_21_values``
        """
        data = data or {}
        batch = self.env["hr.payslip_batch"].browse(docids)
        bruto_rule = self.env["hr.salary_rule"].browse(data.get("bruto_rule_id"))
        pph_rule = self.env["hr.salary_rule"].browse(data.get("pph_rule_id"))
        return batch._prepare_coretax_bupot_21_values(bruto_rule, pph_rule)
