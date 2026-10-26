# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestReportXmlStateGuard(YamlTransactionCase):
    """Scenario tests for the state guard of the Coretax XML report.

    The ``[XML] Coretax`` report must render for a BP21
    (f.1.1.33.01) Out document in ``open`` and ``done`` and keep
    rejecting every other state.
    """

    def test_report_xml_state_guard(self):
        """Draft and confirm are rejected with ``UserError``; open
        (with the default ``/`` name) and done render without
        error."""
        self.run_yaml_scenario("test_report_xml_state_guard.yaml")
