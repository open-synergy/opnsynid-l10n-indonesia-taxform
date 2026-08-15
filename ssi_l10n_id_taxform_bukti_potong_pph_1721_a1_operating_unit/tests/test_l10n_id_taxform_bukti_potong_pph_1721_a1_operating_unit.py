# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestL10nIdTaxformBuktiPotongPph1721A1OperatingUnit(YamlTransactionCase):
    """Scenario tests for the ``operating_unit_id`` field extension on
    ``l10n_id.bukti_potong_pph_1721_a1``."""

    def test_l10n_id_taxform_bukti_potong_pph_1721_a1_operating_unit(self):
        """Run the Operating Unit field extension YAML scenarios."""
        self.run_yaml_scenario(
            "test_data_l10n_id_taxform_bukti_potong_pph_1721_a1_operating_unit.yaml"
        )
