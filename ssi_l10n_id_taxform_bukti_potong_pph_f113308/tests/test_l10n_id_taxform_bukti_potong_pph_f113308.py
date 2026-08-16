# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestL10nIdTaxformBuktiPotongPphF113308(YamlTransactionCase):
    """Scenario test for Bukti Potong PPh 26 (f.1.1.33.08) In/Out."""

    def test_l10n_id_taxform_bukti_potong_pph_f113308(self):
        """Run the create-and-confirm workflow scenario.

        :return: None
        """
        self.run_yaml_scenario(
            "test_data_l10n_id_taxform_bukti_potong_pph_f113308.yaml"
        )
