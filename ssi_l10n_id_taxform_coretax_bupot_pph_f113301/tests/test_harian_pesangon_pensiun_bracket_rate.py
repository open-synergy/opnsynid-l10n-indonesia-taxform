# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHarianPesangonPensiunBracketRate(YamlTransactionCase):
    """Scenario tests for automatic Harian/Pesangon/Pensiun rate
    computation.

    Covers the non-cumulative, per-line bracket lookup added for the
    three tariff types that were previously rejected outright for
    ``rate_computation_method = auto``: Harian (daily wage), Pesangon
    (severance pay), and Pensiun (pension). Each scenario asserts the
    nominal bracket rate at the lower boundary of the taxed layer
    (inclusive, ``<=``), just above it, and mid-bracket — plus
    ``amount_tax`` for the non-boundary points, following ``dpp`` x
    ``rate``.
    """

    def test_harian_pesangon_pensiun_bracket_rate(self):
        """Auto rate for Harian, Pesangon, and Pensiun follows the
        official per-line bracket table, at and around each bracket
        boundary."""
        self.run_yaml_scenario("test_harian_pesangon_pensiun_bracket_rate.yaml")
