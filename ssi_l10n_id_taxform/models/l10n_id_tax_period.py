# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

from odoo import _, api, fields, models


class L10nIdTaxPeriod(models.Model):
    """
    Represents a monthly Indonesian tax period, generated from and
    bounded by a parent tax year (``l10n_id.tax_year``).
    """

    _name = "l10n_id.tax_period"
    _inherit = [
        "mixin.master_data",
        "mixin.date_duration",
    ]
    _description = "Tax Period"
    _order = "date_start asc, id"

    name = fields.Char(
        string="Tax Period",
        required=True,
    )
    year_id = fields.Many2one(
        string="Tax Year",
        comodel_name="l10n_id.tax_year",
        ondelete="cascade",
    )

    def _next_period(self, step):
        """Return the tax period ``step`` positions after this one.

        Searches periods with a later ``date_start`` than this record,
        ordered ascending, and returns the period at index ``step - 1``.

        :param step: 1-based offset counted from the next period onward
        :return: the matching ``l10n_id.tax_period`` record, or
            ``False`` when there is no period that far ahead
        """
        self.ensure_one()
        criteria = [("date_start", ">", self.date_start)]
        results = self.search(criteria)
        if results:
            return results[step - 1]
        return False

    def _previous_period(self, step):
        """Return the tax period ``step`` positions before this one.

        Searches periods with an earlier ``date_start`` than this
        record, ordered descending, and returns the period at index
        ``step - 1``.

        :param step: 1-based offset counted from the previous period
            backward
        :return: the matching ``l10n_id.tax_period`` record, or
            ``False`` when there is no period that far back
        """
        self.ensure_one()
        criteria = [("date_start", "<", self.date_start)]
        results = self.search(criteria, order="date_start desc")
        if results:
            return results[step - 1]
        return False

    @api.model
    def _find_period(self, dt=None, no_raise=False):
        """Find the tax period whose date range contains ``dt``.

        :param dt: date string (``%Y-%m-%d``) to look up; defaults to
            today when not given
        :param no_raise: return ``False`` instead of raising when no
            matching tax period is found
        :return: the matching ``l10n_id.tax_period`` record, or
            ``False`` when ``no_raise`` is set and none is found
        :raises models.ValidationError: when no tax period covers
            ``dt`` and ``no_raise`` is not set
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
            strWarning = _("No tax period configured for %s" % dt)
            raise models.ValidationError(strWarning)
        result = results[0]
        return result
