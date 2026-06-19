# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PayslipBatchCoretaxExport(models.TransientModel):
    _name = "hr.payslip_batch_coretax_export"
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
