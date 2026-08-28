# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestPs17Rate(YamlTransactionCase):
    """Scenario tests for automatic PS17 (Pasal 17) rate computation.

    Covers cumulative-per-tax-year rate lookup for BP21 lines whose
    Coretax Tax Object Code has Tariff Type PS17: the first line for a
    recipient in a tax year (no accumulation), a document cancelled
    before completion (excluded from the accumulation), and a second
    line whose cumulative DPP crosses a bracket boundary.
    """

    def test_ps17_first_bracket(self):
        """Auto rate for a taxpayer with no prior PS17 lines this
        year equals the first bracket rate (0.05)."""
        self.run_yaml_scenario("test_ps17_first_bracket.yaml")

    def test_ps17_cancelled_excluded(self):
        """A cancelled PS17 document does not count toward
        another line's cumulative DPP."""
        self.run_yaml_scenario("test_ps17_cancelled_excluded.yaml")

    def test_ps17_cumulative_cross_bracket(self):
        """Effective rate for a line crossing a bracket boundary
        equals the marginal tax divided by this line's own DPP.

        Pure Python — trigger P2 (L-04: ``odoo_yaml_test`` has no
        float-tolerance assert; the expected effective rate is
        derived here from the same progressive-bracket formula the
        production code uses, so it must be compared with
        ``assertAlmostEqual`` rather than a plain YAML ``value``
        assert).
        """
        tax_year = self.env["l10n_id.tax_year"].create(
            {
                "name": "TY17CROSS",
                "code": "TY17CROSS",
                "date_start": "2039-01-01",
                "date_end": "2039-12-31",
            }
        )
        tax_year.action_create_period()
        tax_period = self.env["l10n_id.tax_period"].search(
            [
                ("year_id", "=", tax_year.id),
                ("date_start", "=", "2039-10-01"),
            ],
            limit=1,
        )
        journal = self.env["account.journal"].create(
            {
                "name": "Test Journal PS17 Cross",
                "code": "TJ17CRS",
                "type": "general",
            }
        )
        account = self.env["account.account"].create(
            {
                "name": "Test PPh 21 Payable PS17 Cross",
                "code": "22402TSTP17C",
                "user_type_id": self.env.ref(
                    "account.data_account_type_current_liabilities"
                ).id,
            }
        )
        tax = self.env["account.tax"].create(
            {
                "name": "PPh 21 PS17 Test Cross",
                "type_tax_use": "purchase",
                "amount": 0.0,
                "amount_type": "percent",
            }
        )
        objek_pajak = self.env["l10n_id.taxform_objek_pajak"].create(
            {
                "code": "21-999-03",
                "name": "Test PS17 Tariff Type Cross",
                "tariff_type": "ps17",
            }
        )
        kpp = self.env["res.partner"].create(
            {"name": "KPP Test PS17 Cross", "is_company": True}
        )
        wajib_pajak = self.env["res.partner"].create(
            {"name": "Test Wajib Pajak PS17 Cross", "is_company": False}
        )
        pemotong_pajak = self.env["res.partner"].create(
            {"name": "PT Test Pemotong Pajak PS17 Cross", "is_company": True}
        )
        rate_table = self.env["l10n_id.pph_21_rate"].create(
            {
                "code": "RATE17CROSS",
                "name": "Rate Table PS17 Cross",
                "date_start": "2039-01-01",
            }
        )
        # UU HPP progressive brackets: 5/15/25/30/35%.
        for min_income, pph_rate in (
            (0.0, 5.0),
            (60000000.0, 15.0),
            (250000000.0, 25.0),
            (500000000.0, 30.0),
            (5000000000.0, 35.0),
        ):
            self.env["l10n_id.pph_21_rate_line"].create(
                {
                    "rate_id": rate_table.id,
                    "min_income": min_income,
                    "pph_rate": pph_rate,
                }
            )

        def create_document(dpp, name_suffix):
            """Create a one-line BP21 document with a fresh move.

            :param dpp: manual DPP amount of the single PS17 line
            :param name_suffix: uniqueness suffix for move/line names
            :return: the created ``l10n_id.bukti_potong_pph_f113301_out``
            """
            move = self.env["account.move"].create(
                {
                    "journal_id": journal.id,
                    "line_ids": [
                        (
                            0,
                            0,
                            {
                                "account_id": account.id,
                                "name": "Test Debit PS17 Cross " + name_suffix,
                                "debit": dpp,
                                "credit": 0.0,
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "account_id": account.id,
                                "name": "Test Credit PS17 Cross " + name_suffix,
                                "debit": 0.0,
                                "credit": dpp,
                            },
                        ),
                    ],
                }
            )
            move_line = move.line_ids.filtered(lambda line_: line_.debit > 0)[:1]
            return self.env["l10n_id.bukti_potong_pph_f113301_out"].create(
                {
                    "date": "2039-10-15",
                    "tax_period_id": tax_period.id,
                    "journal_id": journal.id,
                    "account_id": account.id,
                    "kpp_id": kpp.id,
                    "wajib_pajak_id": wajib_pajak.id,
                    "pemotong_pajak_id": pemotong_pajak.id,
                    "line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": "PS17 Line " + name_suffix,
                                "tax_id": tax.id,
                                "move_line_id": move_line.id,
                                "amount_computation_method": "manual",
                                "manual_amount": dpp,
                                "coretax_tax_object_code": objek_pajak.id,
                                "rate_computation_method": "auto",
                            },
                        )
                    ],
                }
            )

        first_document = create_document(50000000.0, "First")
        first_document.sudo().write({"state": "done"})

        second_document = create_document(20000000.0, "Second")
        second_line = second_document.line_ids[:1]

        def compute_progressive_tax(penghasilan_kena_pajak):
            """Replicate the production progressive-tax formula.

            Independently derived from the UU HPP brackets declared
            above, so the expected value is not just an echo of the
            code under test.

            :param penghasilan_kena_pajak: cumulative taxable income
            :return: cumulative progressive tax on that income
            """
            brackets = [
                (0.0, 5.0),
                (60000000.0, 15.0),
                (250000000.0, 25.0),
                (500000000.0, 30.0),
                (5000000000.0, 35.0),
            ]
            total_tax = 0.0
            for index, (min_income, pph_rate) in enumerate(brackets):
                rate = pph_rate / 100.0
                if penghasilan_kena_pajak <= min_income:
                    continue
                if index + 1 < len(brackets):
                    next_min_income = brackets[index + 1][0]
                    if penghasilan_kena_pajak >= next_min_income:
                        total_tax += rate * (next_min_income - min_income)
                    else:
                        total_tax += rate * (penghasilan_kena_pajak - min_income)
                else:
                    total_tax += rate * (penghasilan_kena_pajak - min_income)
            return total_tax

        cumulative_before = 50000000.0
        cumulative_after = 70000000.0
        expected_rate = (
            compute_progressive_tax(cumulative_after)
            - compute_progressive_tax(cumulative_before)
        ) / 20000000.0

        self.assertAlmostEqual(second_line.rate, expected_rate, places=6)
