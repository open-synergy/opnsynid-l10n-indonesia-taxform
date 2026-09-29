# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestL10nIdTaxformBuktiPotongPphF113301(YamlTransactionCase):
    """YAML-scenario test for Bukti Potong PPh f.1.1.33.01 Out."""

    def test_l10n_id_taxform_bukti_potong_pph_f113301(self):
        """Run create/confirm and cancel/restart policy scenarios.

        Covers the create-and-confirm flow, ``cancel_ok`` restricted
        to state ``done``, and ``restart_ok`` allowed on
        ``confirm``/``open``/``reject`` but not on ``cancel``.
        """
        self.run_yaml_scenario(
            "test_data_l10n_id_taxform_bukti_potong_pph_f113301.yaml"
        )
