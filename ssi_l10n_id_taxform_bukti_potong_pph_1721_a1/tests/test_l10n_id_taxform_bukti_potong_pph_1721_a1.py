# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestL10nIdTaxformBuktiPotongPph1721A1(YamlTransactionCase):
    """Test the ``l10n_id.bukti_potong_pph_1721_a1`` computation flow."""

    def test_l10n_id_taxform_bukti_potong_pph_1721_a1(self):
        """Run the create/compute YAML scenario for Form 1721 A1."""
        self.run_yaml_scenario(
            "test_data_l10n_id_taxform_bukti_potong_pph_1721_a1.yaml"
        )
