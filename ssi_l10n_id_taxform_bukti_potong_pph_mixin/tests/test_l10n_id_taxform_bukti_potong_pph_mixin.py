# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestL10nIdTaxformBuktiPotongPphMixin(YamlTransactionCase):
    """Test ``l10n_id.bukti_potong_pph_type`` master data behaviour.

    Covers create and update of the Bukti Potong PPh form type
    master data provided by this module.
    """

    def test_l10n_id_taxform_bukti_potong_pph_mixin(self):
        """Run the create/update scenarios for ``bukti_potong_pph_type``."""
        self.run_yaml_scenario("test_data_l10n_id_taxform_bukti_potong_pph_mixin.yaml")
