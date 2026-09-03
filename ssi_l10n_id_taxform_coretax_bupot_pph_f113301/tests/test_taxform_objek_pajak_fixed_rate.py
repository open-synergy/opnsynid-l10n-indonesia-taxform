# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestTaxformObjekPajakFixedRate(YamlTransactionCase):
    """Scenario tests for the ``final_flat`` tariff type / ``fixed_rate``.

    Covers automatic rate computation for the 21-402-xx Coretax tax
    object codes (Honorarium/Imbalan Lain APBN/APBD per Golongan), the
    regression guard rejecting automatic computation for a tax object
    code with no Tariff Type set, and the fallback to ``0.0`` (no
    error) once an already-auto line's tax object code is cleared.
    """

    def test_fixed_rate_21_402_02(self):
        """Auto rate for 21-402-02 equals its ``fixed_rate`` (0.05)."""
        self.run_yaml_scenario("test_fixed_rate_21_402_02.yaml")

    def test_fixed_rate_21_402_04(self):
        """Auto rate for 21-402-04 equals its ``fixed_rate`` (0.0)."""
        self.run_yaml_scenario("test_fixed_rate_21_402_04.yaml")

    def test_fixed_rate_rejected_non_final(self):
        """Auto rate is rejected for a line whose tax object code has
        no Tariff Type set."""
        self.run_yaml_scenario("test_fixed_rate_rejected_non_final.yaml")

    def test_rate_auto_without_tax_object_code(self):
        """Auto rate falls back to 0.0, without error, once the tax
        object code is cleared on an already-``auto`` line."""
        self.run_yaml_scenario("test_rate_auto_without_tax_object_code.yaml")
