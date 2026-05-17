# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestL10nIdTaxformPph21Payslip(YamlTransactionCase):
    def test_l10n_id_taxform_pph_21_payslip(self):
        self.run_yaml_scenario("test_data_l10n_id_taxform_pph_21_payslip.yaml")
