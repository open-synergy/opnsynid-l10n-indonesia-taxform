# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestCoretaxBupot21(YamlTransactionCase):
    def setUp(self):
        super().setUp()
        # Withholder (pemotong) identity on the company partner.
        self.company = self.env.ref("base.main_company")
        self.company.partner_id.write(
            {
                "vat": "0029482015507000",
                "nitku": "0029482015507000000000",
            }
        )

        self.journal = self.env["account.journal"].create(
            {"name": "Payroll", "code": "PAYTX", "type": "general"}
        )
        self.payslip_type = self.env["hr.payslip_type"].create(
            {"name": "Monthly Salary", "code": "MONTX"}
        )
        self.structure = self.env["hr.salary_structure"].create(
            {"name": "Test Structure", "code": "STRTX"}
        )
        self.category = self.env["hr.salary_rule_category"].create(
            {"name": "Test Category", "code": "CATTX"}
        )
        self.bruto_rule = self.env["hr.salary_rule"].create(
            {"name": "Gross Income", "code": "BRUTOTX", "category_id": self.category.id}
        )
        self.pph_rule = self.env["hr.salary_rule"].create(
            {"name": "PPh 21", "code": "PPH21TX", "category_id": self.category.id}
        )

        # PTKP category TK/0 ships as data of ssi_l10n_id_taxform_pph_21.
        self.ptkp = self.env["l10n_id.ptkp_category"].search(
            [("code", "=", "TK/0")], limit=1
        )

        # No PPh 21 TER record ships as data; create one for the period so that
        # the rate lookup is deterministic.
        self.ter = self.env["l10n_id.pph_21_ter"].create(
            {
                "name": "TER Test",
                "code": "TERTX",
                "date_start": "2024-01-01",
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "TER A",
                            "code": "A",
                            "ptkp_category_ids": [(6, 0, [self.ptkp.id])],
                            "line_ids": [
                                (0, 0, {"min_income": 0.0, "pph_rate": 5.0}),
                            ],
                        },
                    )
                ],
            }
        )

        # Employee subject to PPh 21 (withheld tax > 0).
        self.partner_taxed = self.env["res.partner"].create(
            {
                "name": "Employee Taxed - Home",
                "vat": "3275010905770021",
                "ptkp_category_id": self.ptkp.id,
            }
        )
        self.job = self.env["hr.job"].create({"name": "Staff"})
        self.employee_taxed = self.env["hr.employee"].create(
            {
                "name": "Employee Taxed",
                "address_home_id": self.partner_taxed.id,
                "job_id": self.job.id,
            }
        )

        # Employee NOT subject to PPh 21 (withheld tax == 0).
        self.partner_free = self.env["res.partner"].create(
            {
                "name": "Employee Free - Home",
                "vat": "1403011006750026",
                "ptkp_category_id": self.ptkp.id,
            }
        )
        self.employee_free = self.env["hr.employee"].create(
            {
                "name": "Employee Free",
                "address_home_id": self.partner_free.id,
            }
        )

        self.batch = self.env["hr.payslip_batch"].create(
            {
                "type_id": self.payslip_type.id,
                "company_id": self.company.id,
                "date": "2024-10-31",
                "date_start": "2024-10-01",
                "date_end": "2024-10-31",
            }
        )
        self.payslip_taxed = self._create_payslip(
            self.employee_taxed, gross=40000000.0, pph=2000000.0
        )
        self.payslip_free = self._create_payslip(
            self.employee_free, gross=5000000.0, pph=0.0
        )

    def _create_payslip(self, employee, gross, pph):
        return self.env["hr.payslip"].create(
            {
                "batch_id": self.batch.id,
                "employee_id": employee.id,
                "type_id": self.payslip_type.id,
                "structure_id": self.structure.id,
                "journal_id": self.journal.id,
                "date": "2024-10-21",
                "date_start": "2024-10-01",
                "date_end": "2024-10-31",
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "rule_id": self.bruto_rule.id,
                            "amount": gross,
                            "quantity": 1.0,
                            "rate": 100.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "rule_id": self.pph_rule.id,
                            "amount": pph,
                            "quantity": 1.0,
                            "rate": 100.0,
                        },
                    ),
                ],
            }
        )

    def test_format_number(self):
        """Integer-valued numbers are rendered without a trailing ``.0``."""
        self.assertEqual(self.batch._coretax_format_number(40000000.0), "40000000")
        self.assertEqual(self.batch._coretax_format_number(5.5), "5.5")

    def test_only_taxed_employee_exported(self):
        """Only payslips whose withheld PPh 21 is greater than zero are
        included, and the header/slip fields are mapped to the BPMP schema."""
        values = self.batch._prepare_coretax_bupot_21_values(
            self.bruto_rule, self.pph_rule
        )

        # Header (pemotong) data.
        self.assertEqual(values["company_tin"], "0029482015507000")
        self.assertEqual(values["company_id_tku"], "0029482015507000000000")

        # The PPh 21-free employee must be filtered out.
        self.assertEqual(len(values["slips"]), 1)
        slip = values["slips"][0]

        self.assertEqual(slip["counterpart_tin"], "3275010905770021")
        self.assertEqual(slip["counterpart_opt"], "Resident")
        self.assertEqual(slip["status_tax_exemption"], "TK/0")
        self.assertEqual(slip["position"], self.employee_taxed.job_id.name or "")
        self.assertEqual(slip["tax_object_code"], "21-100-01")
        self.assertEqual(slip["tax_certificate"], "N/A")
        self.assertEqual(slip["gross"], "40000000")
        self.assertEqual(slip["tax_period_month"], 10)
        self.assertEqual(slip["tax_period_year"], 2024)
        self.assertEqual(slip["withholding_date"], "2024-10-21")
        self.assertEqual(
            slip["id_place_of_business_activity"], "0029482015507000000000"
        )

        # The rate must come from the PPh 21 TER table.
        expected_rate = (
            self.env["l10n_id.pph_21_ter"]
            .find(self.payslip_taxed.date)
            .compute_tax(40000000.0, [self.ptkp.id])["rate"]
        )
        self.assertEqual(slip["rate"], self.batch._coretax_format_number(expected_rate))

    def test_missing_employee_npwp_raises(self):
        """A taxed employee without NPWP/PTKP must raise a user error."""
        self.partner_taxed.write({"vat": False})
        with self.assertRaises(UserError):
            self.batch._prepare_coretax_bupot_21_values(self.bruto_rule, self.pph_rule)

    def test_missing_company_identity_raises(self):
        """A withholder company without NPWP/NITKU must raise a user error."""
        self.company.partner_id.write({"nitku": False})
        with self.assertRaises(UserError):
            self.batch._prepare_coretax_bupot_21_values(self.bruto_rule, self.pph_rule)

    def test_no_taxed_payslip_raises(self):
        """A batch where no payslip has PPh 21 withheld must raise an error."""
        self.payslip_taxed.line_ids.filtered(
            lambda line: line.rule_id == self.pph_rule
        ).write({"amount": 0.0})
        with self.assertRaises(UserError):
            self.batch._prepare_coretax_bupot_21_values(self.bruto_rule, self.pph_rule)
