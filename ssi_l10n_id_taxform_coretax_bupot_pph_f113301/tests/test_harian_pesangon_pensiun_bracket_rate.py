# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHarianPesangonPensiunBracketRate(YamlTransactionCase):
    """Scenario tests for automatic Harian/Pesangon/Pensiun rate and
    tax amount computation.

    Covers the non-cumulative, per-line bracket lookup added for the
    three tariff types that were previously rejected outright for
    ``rate_computation_method = auto``: Harian (daily wage), Pesangon
    (severance pay), and Pensiun (pension). Each rate scenario
    asserts the nominal bracket rate at the lower boundary of the
    taxed layer (inclusive, ``<=``), just above it, and mid-bracket.
    For Harian, ``amount_tax`` follows the flat ``dpp`` x ``rate``
    formula; for Pesangon/Pensiun it is marginal/layered across the
    bracket table, not flat, so mid-bracket points assert the
    layered amount rather than ``dpp`` x nominal rate. Two further
    scenarios cover the shared 0%-tariff fallback fix: a 0% auto
    lookup never falls back to ``tax_id.compute_all()``, and a
    document whose only line is such a 0% line can still be saved.
    """

    def test_harian_pesangon_pensiun_bracket_rate(self):
        """Auto rate for Harian, Pesangon, and Pensiun follows the
        official per-line bracket table, at and around each bracket
        boundary."""
        self.run_yaml_scenario("test_harian_pesangon_pensiun_bracket_rate.yaml")
