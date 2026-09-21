# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestManualNumberCoretax(YamlTransactionCase):
    """Scenario tests for manually assigning the Coretax document
    number on a BP21 (f.1.1.33.01) Out document while it is Waiting
    for Approval, and for confirming that the internal sequence no
    longer overrides it on ``action_done``.
    """

    def test_manual_number_kept_through_done(self):
        """A ``name`` typed manually while ``confirm`` survives
        ``action_done`` unchanged."""
        self.run_yaml_scenario("test_manual_number_coretax_kept.yaml")

    def test_default_number_not_auto_assigned(self):
        """A document confirmed without a manual ``name`` keeps the
        default ``"/"`` through ``action_done``, proving
        ``_create_sequence_state = False`` disables the sequence."""
        self.run_yaml_scenario("test_manual_number_coretax_default.yaml")
