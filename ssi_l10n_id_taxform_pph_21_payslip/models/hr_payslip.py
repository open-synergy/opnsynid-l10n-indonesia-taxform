# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    @api.depends(
        "employee_id",
        "date",
    )
    def _compute_payslip_tax_period(self):
        for payslip in self:
            obj_period = self.env["l10n_id.tax_period"]
            payslip.joining_tax_month = 1
            try:
                period = obj_period._find_period(payslip.date)
                payslip.tax_period_id = period
                payslip.tax_year_id = period.year_id
            except Exception:
                payslip.tax_period_id = False
                payslip.tax_year_id = False
                continue

            if not payslip.tax_period_id:
                continue

            employee = payslip.employee_id
            if employee.joining_tax_year_id == payslip.tax_year_id:
                payslip.joining_tax_month = (
                    employee.joining_tax_period_id.date_start.month
                )

    joining_tax_month = fields.Integer(
        string="Joining Tax Month",
        compute="_compute_payslip_tax_period",
        store=True,
    )
    tax_period_id = fields.Many2one(
        string="Payslip Tax Period",
        comodel_name="l10n_id.tax_period",
        compute="_compute_payslip_tax_period",
        store=True,
    )
    tax_year_id = fields.Many2one(
        string="Payslip Tax Year",
        comodel_name="l10n_id.tax_year",
        compute="_compute_payslip_tax_period",
        store=True,
    )
