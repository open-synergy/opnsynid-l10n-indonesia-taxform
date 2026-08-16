# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrPayslipBatchCoretaxExport(models.TransientModel):
    """Collect the two salary rules and export the Coretax BPMP XML.

    Opened from the ``hr.payslip_batch`` Export Coretax PPh 21 XML button,
    this wizard asks which salary rule holds the gross income and which one
    holds the withheld PPh 21, then triggers the ``bpmp`` report download
    for the batch.
    """

    _name = "hr_payslip_batch_coretax_export"
    _description = "Export Coretax PPh 21 Withholding XML"

    batch_id = fields.Many2one(
        string="Payslip Batch",
        comodel_name="hr.payslip_batch",
        required=True,
        readonly=True,
        default=lambda self: self.env.context.get("active_id"),
        help="Payslip batch whose payslips are exported to Coretax BPMP XML.",
    )
    bruto_rule_id = fields.Many2one(
        string="Gross Income Salary Rule",
        comodel_name="hr.salary_rule",
        required=True,
        help="Salary rule whose amount is reported as the gross income "
        "(Penghasilan Bruto) of each Coretax withholding slip.",
    )
    pph_rule_id = fields.Many2one(
        string="Withheld PPh 21 Salary Rule",
        comodel_name="hr.salary_rule",
        required=True,
        help="Salary rule whose amount is the withheld PPh 21. Only payslips "
        "where this amount is greater than zero are exported.",
    )

    def action_export(self):
        """Validate the batch data, then trigger the Coretax XML download.

        :return: an ``ir.actions.report`` dict rendering the ``bpmp``
            report for ``batch_id``
        :raises odoo.exceptions.UserError: when the withholder company or a
            taxed employee is missing required data, or no payslip in the
            batch has PPh 21 withheld (raised by
            ``hr.payslip_batch._prepare_coretax_bupot_21_values``)
        """
        self.ensure_one()
        # Validate the data up front so configuration problems surface as a
        # clean user error instead of a download failure.
        self.batch_id._prepare_coretax_bupot_21_values(
            self.bruto_rule_id, self.pph_rule_id
        )
        data = {
            "bruto_rule_id": self.bruto_rule_id.id,
            "pph_rule_id": self.pph_rule_id.id,
        }
        report = self.env.ref(
            "ssi_l10n_id_taxform_coretax_bupot_21_payslip_batch."
            "coretax_bupot_21_report_action"
        )
        return report.report_action(self.batch_id, data=data)
