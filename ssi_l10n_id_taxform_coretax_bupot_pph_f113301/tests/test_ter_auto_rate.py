# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestTerAutoRate(YamlTransactionCase):
    """Scenario tests for automatic TER rate computation.

    Covers the scale of ``_get_auto_ter_rate()``'s return value: it
    must be a fraction (e.g. ``0.06`` for 6%), consistent with
    ``manual_rate``/``fixed_rate``/``_get_ps17_bracket_rate``, rather
    than the raw percentage (``6.0``) that
    ``Pph21TerLine.compute_tax()`` returns as its own ``rate`` key.
    """

    def test_ter_auto_rate(self):
        """A DPP landing in a bracket above 0% computes ``rate`` as a
        fraction and ``amount_tax`` as ``dpp`` x ``rate``."""
        self.run_yaml_scenario("test_ter_auto_rate.yaml")

    def test_ter_auto_rate_below_ptkp(self):
        """A DPP landing in the 0% bracket (below PTKP) computes
        both ``rate`` and ``amount_tax`` as zero."""
        self.run_yaml_scenario("test_ter_auto_rate_below_ptkp.yaml")
