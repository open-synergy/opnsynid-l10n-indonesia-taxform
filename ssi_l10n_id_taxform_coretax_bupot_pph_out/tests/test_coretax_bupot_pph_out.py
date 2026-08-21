# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestCoretaxBupotPPhOut(YamlTransactionCase):
    """Cover the Coretax XML export for an outgoing Bukti Potong PPh 23.

    Exercises ``_coretax_format_number``,
    ``_prepare_coretax_bupot_pph_out_values``, and the ``UserError``
    guards raised when the withholder or wajib pajak identity data
    required by the DGT Coretax XML schema is missing.
    """

    def setUp(self):
        """Create one PPh 23 Bukti Potong with a taxed line.

        Sets NPWP/NITKU on the company (pemotong) partner, creates a
        domestic wajib pajak with NPWP, and creates the KPP, tax
        period, journal, account, move, and tax records needed to
        confirm a ``l10n_id.bukti_potong_pph_f113306_out`` with one
        line tagged with ``coretax_tax_object_code``.
        """
        super().setUp()

        # Withholder (pemotong) identity on the company partner.
        self.company = self.env.ref("base.main_company")
        self.company.partner_id.write(
            {
                "vat": "0029482015507000",
                "nitku": "0029482015507000000000",
            }
        )

        # Wajib pajak (income recipient) — domestic, with NPWP.
        self.wajib_pajak = self.env["res.partner"].create(
            {
                "name": "PT Wajib Pajak Test",
                "is_company": True,
                "vat": "0123456789012000",
            }
        )

        # KPP (tax office) partner.
        self.kpp = self.env["res.partner"].create(
            {
                "name": "KPP Pratama Test",
                "is_company": True,
            }
        )

        # Tax period.
        self.tax_year = self.env["l10n_id.tax_year"].create(
            {
                "name": "2024",
                "code": "2024",
                "date_start": "2024-01-01",
                "date_end": "2024-12-31",
            }
        )
        self.tax_year.action_create_period()
        self.tax_period = self.env["l10n_id.tax_period"].search(
            [
                ("year_id", "=", self.tax_year.id),
                ("date_start", "=", "2024-10-01"),
            ],
            limit=1,
        )

        # General journal for accounting entries.
        self.journal = self.env["account.journal"].create(
            {"name": "Test General", "code": "TSTBPG", "type": "general"}
        )

        # Account for the bukti potong.
        self.account = self.env["account.account"].create(
            {
                "name": "Test PPh 23 Payable",
                "code": "22401TST",
                "user_type_id": self.env.ref(
                    "account.data_account_type_current_liabilities"
                ).id,
            }
        )

        # Account move with a line used as move_line_id on the bukti potong line.
        self.move = self.env["account.move"].create(
            {
                "journal_id": self.journal.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.account.id,
                            "name": "Test Debit",
                            "debit": 10000000.0,
                            "credit": 0.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "account_id": self.account.id,
                            "name": "Test Credit",
                            "debit": 0.0,
                            "credit": 10000000.0,
                        },
                    ),
                ],
            }
        )
        self.move_line = self.move.line_ids.filtered(lambda l: l.debit > 0)[0]

        # PPh 23 tax at 2%.
        self.tax = self.env["account.tax"].create(
            {
                "name": "PPh 23 2% Test",
                "type_tax_use": "purchase",
                "amount": 2.0,
                "amount_type": "percent",
            }
        )

        # Bukti Potong PPh 23 Out record with one line.
        self.bukpot = self.env["l10n_id.bukti_potong_pph_f113306_out"].create(
            {
                "date": "2024-10-15",
                "tax_period_id": self.tax_period.id,
                "journal_id": self.journal.id,
                "account_id": self.account.id,
                "kpp_id": self.kpp.id,
                "wajib_pajak_id": self.wajib_pajak.id,
                "pemotong_pajak_id": self.company.partner_id.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Test Line PPh 23",
                            "tax_id": self.tax.id,
                            "move_line_id": self.move_line.id,
                            "amount_computation_method": "manual",
                            "manual_amount": 10000000.0,
                            "coretax_tax_object_code": "23-100-01",
                        },
                    )
                ],
            }
        )

    def test_format_number(self):
        """Integer-valued numbers are rendered without a trailing ``.0``."""
        self.assertEqual(self.bukpot._coretax_format_number(10000000.0), "10000000")
        self.assertEqual(self.bukpot._coretax_format_number(2.5), "2.5")

    def test_prepare_values_header(self):
        """Header fields (TIN, ID TKU) are mapped from pemotong_pajak_id."""
        values = self.bukpot._prepare_coretax_bupot_pph_out_values()
        self.assertEqual(values["company_tin"], "0029482015507000")
        self.assertEqual(values["company_id_tku"], "0029482015507000000000")

    def test_prepare_values_line(self):
        """Line data is correctly mapped from the bukti potong line."""
        values = self.bukpot._prepare_coretax_bupot_pph_out_values()
        self.assertEqual(len(values["lines"]), 1)
        line = values["lines"][0]
        self.assertEqual(line["counterpart_tin"], "0123456789012000")
        self.assertEqual(line["counterpart_opt"], "Resident")
        self.assertEqual(line["tax_object_code"], "23-100-01")
        self.assertEqual(line["gross"], "10000000")
        self.assertEqual(line["tax_period_month"], 10)
        self.assertEqual(line["tax_period_year"], 2024)
        self.assertEqual(line["withholding_date"], "2024-10-15")
        self.assertEqual(
            line["id_place_of_business_activity"], "0029482015507000000000"
        )

    def test_zero_tax_line_excluded(self):
        """Lines with zero or negative amount_tax must be excluded from the
        export."""
        # Add a second line with zero manual_amount so amount_tax stays 0.
        self.bukpot.write(
            {
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Zero Tax Line",
                            "tax_id": self.tax.id,
                            "move_line_id": self.move_line.id,
                            "amount_computation_method": "manual",
                            "manual_amount": 0.0,
                            "coretax_tax_object_code": "23-100-01",
                        },
                    )
                ]
            }
        )
        values = self.bukpot._prepare_coretax_bupot_pph_out_values()
        # Only the original line with amount_tax > 0 should appear.
        self.assertEqual(len(values["lines"]), 1)

    def test_missing_pemotong_npwp_raises(self):
        """A withholder without NPWP must raise a UserError."""
        self.company.partner_id.write({"vat": False})
        with self.assertRaises(UserError):
            self.bukpot._prepare_coretax_bupot_pph_out_values()

    def test_missing_pemotong_nitku_raises(self):
        """A withholder without NITKU must raise a UserError."""
        self.company.partner_id.write({"nitku": False})
        with self.assertRaises(UserError):
            self.bukpot._prepare_coretax_bupot_pph_out_values()

    def test_missing_wajib_pajak_npwp_raises(self):
        """A wajib pajak without NPWP must raise a UserError."""
        self.wajib_pajak.write({"vat": False})
        with self.assertRaises(UserError):
            self.bukpot._prepare_coretax_bupot_pph_out_values()

    def test_no_taxed_line_raises(self):
        """A bukti potong with no line having positive amount_tax must raise."""
        self.bukpot.line_ids.write({"manual_amount": 0.0})
        with self.assertRaises(UserError):
            self.bukpot._prepare_coretax_bupot_pph_out_values()

    def test_non_resident_counterpart_opt(self):
        """A foreign wajib pajak must produce CounterpartOpt = NonResident."""
        singapore = self.env["res.country"].search([("code", "=", "SG")], limit=1)
        if singapore:
            self.wajib_pajak.write({"country_id": singapore.id})
            values = self.bukpot._prepare_coretax_bupot_pph_out_values()
            self.assertEqual(values["lines"][0]["counterpart_opt"], "NonResident")
