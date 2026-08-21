# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class HrEmployee(models.Model):
    """
    Adds Indonesian PPh 21 joining tax period tracking to the employee.
    Determines which tax period/year the employee's join date falls into,
    so payslip PPh 21 computation can tell whether the payslip period is
    the employee's first tax year of employment.
    """

    _inherit = "hr.employee"

    @api.depends(
        "date_join",
    )
    def _compute_tax_period(self):
        """Resolve the tax period/year matching ``date_join``.

        Looks up the ``l10n_id.tax_period`` that contains the employee's
        join date and stores it, along with its parent tax year, on
        ``joining_tax_period_id``/``joining_tax_year_id``. Both fields are
        left empty when ``date_join`` is not set or falls outside any
        configured tax period.
        """
        for employee in self:
            joining_tax_period_id = False
            joining_tax_year_id = False

            date_join = employee.sudo().date_join
            if date_join:
                obj_period = self.env["l10n_id.tax_period"].sudo()
                period = obj_period._find_period(date_join, no_raise=True)
                if period:
                    joining_tax_period_id = period
                    joining_tax_year_id = period.year_id

            employee.joining_tax_period_id = joining_tax_period_id
            employee.joining_tax_year_id = joining_tax_year_id

    joining_tax_period_id = fields.Many2one(
        string="Joining Tax Period",
        comodel_name="l10n_id.tax_period",
        compute="_compute_tax_period",
        store=True,
        compute_sudo=True,
    )
    joining_tax_year_id = fields.Many2one(
        string="Joining Tax Year",
        comodel_name="l10n_id.tax_year",
        compute="_compute_tax_period",
        store=True,
        compute_sudo=True,
    )
