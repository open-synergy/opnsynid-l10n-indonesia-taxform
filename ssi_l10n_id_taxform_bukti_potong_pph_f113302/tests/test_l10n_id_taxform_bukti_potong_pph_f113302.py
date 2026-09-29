# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestL10nIdTaxformBuktiPotongPphF113302(YamlTransactionCase):
    """YAML-scenario test for Bukti Potong PPh f.1.1.33.02 Out."""

    def test_l10n_id_taxform_bukti_potong_pph_f113302(self):
        """Run the create/confirm/approve/done and policy scenarios.

        Covers the create-and-confirm flow, the positive path of a
        manual number kept through ``done``, the negative path of an
        auto-assigned sequence number unchanged after ``done``,
        ``cancel_ok`` restricted to state ``done``, and
        ``restart_ok`` allowed on ``confirm``/``open``/``reject`` but
        not on ``cancel``.
        """
        self.run_yaml_scenario(
            "test_data_l10n_id_taxform_bukti_potong_pph_f113302.yaml"
        )
