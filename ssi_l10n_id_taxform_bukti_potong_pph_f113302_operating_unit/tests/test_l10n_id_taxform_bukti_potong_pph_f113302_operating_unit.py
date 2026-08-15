# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestL10nIdTaxformBuktiPotongPphF113302OperatingUnit(YamlTransactionCase):
    """Test the operating unit fields on Bukti Potong PPh f.1.1.33.02
    Out.

    Runs the YAML scenario that exercises the ``operating_unit_id``
    field added by ``mixin.single_operating_unit``.
    """

    def test_l10n_id_taxform_bukti_potong_pph_f113302_operating_unit(self):
        """Run the operating unit YAML scenario.

        :return: None
        """
        self.run_yaml_scenario(
            "test_data_l10n_id_taxform_bukti_potong_pph_f113302_operating_unit.yaml"
        )
