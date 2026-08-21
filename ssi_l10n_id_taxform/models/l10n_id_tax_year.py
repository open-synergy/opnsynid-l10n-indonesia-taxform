# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class L10nIdTaxYear(models.Model):
    """
    Represents an Indonesian tax year, used to bound and generate the
    monthly tax periods (``l10n_id.tax_period``) that fall within it.
    """

    _name = "l10n_id.tax_year"
    _inherit = [
        "mixin.master_data",
        "mixin.date_duration",
    ]
    _description = "Tax Year"
    _order = "date_start asc, id"

    name = fields.Char(
        string="Tax Year",
        required=True,
    )
    period_ids = fields.One2many(
        string="Periods",
        comodel_name="l10n_id.tax_period",
        inverse_name="year_id",
    )

    def action_create_period(self):
        """Generate the monthly tax periods for each selected tax year.

        Triggers ``_create_period`` for every record in ``self``.
        """
        for year in self:
            year._create_period()

    def _create_period(self):
        """Create one ``l10n_id.tax_period`` record per calendar month.

        Iterates from ``date_start`` to ``date_end`` in one-month steps,
        clamping the last period's ``date_end`` to the tax year's
        ``date_end`` when it would otherwise overflow. Each generated
        period is linked back to this tax year via ``year_id``.

        :raises UserError: if a computed period's end date ends up
            before its start date
        """
        self.ensure_one()
        obj_period = self.env["l10n_id.tax_period"]
        date_start = self.date_start
        while date_start < self.date_end:
            date_end = date_start + relativedelta(months=+1, days=-1)

            if date_end > self.date_end:
                date_end = self.date_end

            if date_end < date_start:
                strWarning = _(
                    "Date Start "
                    + date_start.strftime("%Y-%m-%d")
                    + " > Date End "
                    + date_end.strftime("%Y-%m-%d")
                )
                raise UserError(strWarning)

            obj_period.create(
                {
                    "name": date_start.strftime("%m/%Y"),
                    "code": date_start.strftime("%m/%Y"),
                    "date_start": date_start.strftime("%Y-%m-%d"),
                    "date_end": date_end.strftime("%Y-%m-%d"),
                    "year_id": self.id,
                }
            )
            date_start = date_start + relativedelta(months=+1)

    @api.model
    def _find_year(self, dt=None, no_raise=False):
        """Find the tax year whose date range contains ``dt``.

        :param dt: date string (``%Y-%m-%d``) to look up; defaults to
            today when not given
        :param no_raise: return ``False`` instead of raising when no
            matching tax year is found
        :return: the matching ``l10n_id.tax_year`` record, or ``False``
            when ``no_raise`` is set and none is found
        :raises models.ValidationError: when no tax year covers ``dt``
            and ``no_raise`` is not set
        """
        if not dt:
            dt = datetime.now().strftime("%Y-%m-%d")
        criteria = [
            ("date_start", "<=", dt),
            ("date_end", ">=", dt),
        ]
        results = self.search(criteria)
        if not results:
            if no_raise:
                return False
            strWarning = _("No tax year configured for %s" % dt)
            raise models.ValidationError(strWarning)
        result = results[0]
        return result
