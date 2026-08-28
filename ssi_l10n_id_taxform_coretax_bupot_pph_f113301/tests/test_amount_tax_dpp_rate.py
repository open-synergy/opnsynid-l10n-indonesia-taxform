# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAmountTaxDppRate(YamlTransactionCase):
    """Scenario tests for ``amount_tax`` computed from ``dpp`` x ``rate``.

    Covers the BP21 f.1.1.33.01 Out line override that derives
    ``amount_tax`` from this line's own ``dpp``/``rate`` instead of
    ``tax_id.compute_all()``, so a ``tax_id`` deliberately set to 0%
    (to avoid double-counting a rate already captured by ``dpp``/
    ``rate``) no longer forces ``amount_tax`` to 0.
    """

    def test_amount_tax_from_dpp_rate(self):
        """``amount_tax`` follows ``dpp`` x ``rate`` and stays in sync
        after ``manual_rate`` is written."""
        self.run_yaml_scenario("test_amount_tax_from_dpp_rate.yaml")

    def test_amount_tax_zero_rate_rejected(self):
        """A line with ``manual_rate = 0.0`` still yields
        ``amount_tax == 0.0`` and is rejected by
        ``_constrains_total_tax_final`` (existing behaviour,
        unchanged by the ``dpp`` x ``rate`` override)."""
        self.run_yaml_scenario("test_amount_tax_zero_rate_rejected.yaml")
