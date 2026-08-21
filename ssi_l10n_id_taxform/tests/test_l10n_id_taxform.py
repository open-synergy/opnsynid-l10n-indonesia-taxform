# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestL10nIdTaxform(YamlTransactionCase):
    """
    Cover ``l10n_id.tax_year``, ``l10n_id.tax_period``, and
    ``l10n_id.taxform_objek_pajak`` creation, period generation, and
    period/year lookup helpers.
    """

    def test_l10n_id_taxform(self):
        """Run the tax year/period/objek pajak YAML scenario."""
        self.run_yaml_scenario("test_data_l10n_id_taxform.yaml")
