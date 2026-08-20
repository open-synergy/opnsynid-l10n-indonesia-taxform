# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestEfakturOfDppLainFakturPajakKeluaran(YamlTransactionCase):
    """Scenario tests for the Coretax ``OtherTaxBase`` (OFS/26/000029).

    Covers the new ``efaktur_of_dpp_lain`` field (detail and header
    level), which back-computes the "DPP Nilai Lain" adjusted tax base
    from ``price_tax``/``amount_tax`` since the adjusted base itself
    is only a local variable inside the tax's ``python_compute``
    snippet and is never exposed on any field. The Coretax XML render
    check (``<OtherTaxBase>`` using the new field instead of the raw
    ``efaktur_of_dpp``) is covered separately in Python -- see
    ``test_core_tax_report_renders_other_tax_base`` below.
    """

    def test_efaktur_of_dpp_lain_faktur_pajak_keluaran(self):
        """Run the DPP Nilai Lain back-computation scenario."""
        self.run_yaml_scenario(
            "test_data_faktur_pajak_keluaran_efaktur_of_dpp_lain.yaml"
        )

    def test_core_tax_report_renders_other_tax_base(self):
        """Render ``core_tax_xml_report`` and check ``OtherTaxBase``.

        Written in Python, not YAML: rendering a ``qweb-xml`` report
        and inspecting its output bytes is outside the six actions
        (``create``/``write``/``call``/``assert``/``ref``/``search``)
        the installed ``odoo-yaml-test`` (0.1.0) implements -- there
        is no action that calls ``ir.actions.report`` methods or lets
        an assertion inspect a rendered string.

        Trigger/limitation: P8 (rendering a report and asserting its
        content), L-19 in ``python-escape-hatch.md`` -- report
        rendering has no YAML-expressible form regardless of library
        version.
        """
        revenue_type = self.env.ref("account.data_account_type_revenue")
        liability_type = self.env.ref(
            "account.data_account_type_current_liabilities"
        )
        income_account = self.env["account.account"].create(
            {
                "code": "FPKDLR1",
                "name": "Test Report DPP Lain FPK Income",
                "user_type_id": revenue_type.id,
            }
        )
        tax_account = self.env["account.account"].create(
            {
                "code": "FPKDLR2",
                "name": "Test Report DPP Lain FPK VAT Payable",
                "user_type_id": liability_type.id,
            }
        )
        tax_dpp_lain = self.env["account.tax"].create(
            {
                "name": "Test Report DPP Lain FPK VAT",
                "amount_type": "code",
                "amount": 11.0,
                "type_tax_use": "sale",
                "python_compute": (
                    "DPP = (11.0/12.0) * price_unit * quantity\n"
                    "DPP = round(DPP,2)\n"
                    "PPN = DPP * 0.12\n"
                    "PPN = round(PPN, 0)\n"
                    "result = PPN"
                ),
                "invoice_repartition_line_ids": [
                    (0, 0, {"factor_percent": 100, "repartition_type": "base"}),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "tax",
                            "account_id": tax_account.id,
                        },
                    ),
                ],
                "refund_repartition_line_ids": [
                    (0, 0, {"factor_percent": 100, "repartition_type": "base"}),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "tax",
                            "account_id": tax_account.id,
                        },
                    ),
                ],
            }
        )
        fp_type_open = self.env["faktur_pajak_transaction_type"].create(
            {
                "name": "Test Report DPP Lain FPK Type",
                "code": "/",
                "efaktur_mode": "detail",
                "fpk_journal_selection_method": "domain",
                "tax_id": tax_dpp_lain.id,
            }
        )
        partner = self.env["res.partner"].create(
            {"name": "Test Report DPP Lain FPK Partner", "is_company": True}
        )
        fpk = self.env["faktur_pajak_keluaran"].create(
            {
                "type_id": fp_type_open.id,
                "tax_id": tax_dpp_lain.id,
                "partner_id": partner.id,
                "date": "2026-01-15",
                "efaktur_mode": "detail",
            }
        )
        detail = self.env["faktur_pajak_keluaran_detail"].create(
            {
                "faktur_pajak_keluaran_id": fpk.id,
                "name": "Test Report DPP Lain FPK Line",
                "account_id": income_account.id,
                "uom_quantity": 1,
                "price_unit": 50000000.0,
                "tax_ids": [(6, 0, [tax_dpp_lain.id])],
            }
        )

        self.assertEqual(detail.efaktur_of_dpp_lain, "45833333")
        self.assertAlmostEqual(
            int(detail.efaktur_of_dpp_lain) * 0.12,
            detail.price_tax,
            delta=1.0,
            msg=(
                "back-computed OtherTaxBase, re-multiplied by the VAT "
                "rate, must land within rounding tolerance of the "
                "actual VAT amount"
            ),
        )

        report = self.env.ref(
            "ssi_l10n_id_taxform_faktur_pajak.core_tax_xml_report"
        )
        content, _report_type = report._render_qweb_xml(fpk.ids)
        xml_text = (
            content.decode("utf-8") if isinstance(content, bytes) else content
        )

        self.assertIn(
            "<OtherTaxBase>45833333</OtherTaxBase>",
            xml_text,
            "rendered Coretax XML must carry the back-computed "
            "OtherTaxBase",
        )
        self.assertNotIn(
            "<OtherTaxBase>50000000.0</OtherTaxBase>",
            xml_text,
            "rendered Coretax XML must not fall back to the raw "
            "untaxed amount (the original reported bug)",
        )
