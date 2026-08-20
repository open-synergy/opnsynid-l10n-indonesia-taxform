# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import ValidationError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestActionComputeTaxFakturPajakKeluaran(YamlTransactionCase):
    """Scenario tests for ``faktur_pajak_keluaran`` tax recomputation.

    Covers ``action_compute_tax`` recalculating the header tax summary
    (``tax_ids``/``amount_tax``) from taxes edited manually on
    ``detail_ids``, and the ``pre_confirm_action`` hook doing the same
    automatically before confirmation. The tax-vs-transaction-type
    ``@api.constrains`` guard is covered separately in Python -- see
    ``test_tax_not_allowed_by_type_is_rejected`` below.
    """

    def test_action_compute_tax_faktur_pajak_keluaran(self):
        """Run the tax recompute and pre_confirm_action scenarios."""
        self.run_yaml_scenario(
            "test_data_faktur_pajak_keluaran_action_compute_tax.yaml"
        )

    def test_tax_not_allowed_by_type_is_rejected(self):
        """Reject a tax outside the transaction type's whitelist.

        Written in Python, not YAML: the ``odoo-yaml-test`` version
        actually installed in this environment (0.1.0) has no
        ``expect_error`` key at all -- it was only added upstream in
        0.4.0, which the project's skill documentation assumes as the
        baseline but is not what is pinned/cached in this container's
        image. Confirmed by inspecting the installed package's
        ``case.py``: none of ``_action_create``/``_action_write``/
        ``_action_call`` reads or branches on an ``expect_error`` key,
        so a step meant to raise would simply crash the whole
        scenario instead of being asserted as an expected failure.
        Negative-path testing of ``@api.constrains`` therefore has no
        YAML-expressible form here, so it is written directly against
        the ORM with ``assertRaises`` instead.

        Trigger/limitation: P5-adjacent, L-27 (both uncatalogued in
        ``python-escape-hatch.md`` as of this writing -- the catalog
        assumes ``expect_error`` exists at all, with caveats; L-27 is
        the sharper case of it not existing in the installed version
        in the first place).
        """
        revenue_type = self.env.ref("account.data_account_type_revenue")
        liability_type = self.env.ref("account.data_account_type_current_liabilities")
        income_account = self.env["account.account"].create(
            {
                "code": "FPKVAL1",
                "name": "Test Tax Validation FPK Income",
                "user_type_id": revenue_type.id,
            }
        )
        tax_account = self.env["account.account"].create(
            {
                "code": "FPKVAL2",
                "name": "Test Tax Validation FPK VAT Payable",
                "user_type_id": liability_type.id,
            }
        )

        def make_tax(name, amount):
            """Create a percent output VAT with a tax repartition account.

            :param name: tax display name
            :param amount: tax rate, e.g. ``12.0`` for 12%
            :return: the created ``account.tax`` record
            """
            return self.env["account.tax"].create(
                {
                    "name": name,
                    "amount_type": "percent",
                    "amount": amount,
                    "type_tax_use": "sale",
                    "price_include": False,
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

        tax_12 = make_tax("Test Tax Validation FPK VAT 12pct", 12.0)
        tax_11 = make_tax("Test Tax Validation FPK VAT 11pct", 11.0)

        fp_type_restricted = self.env["faktur_pajak_transaction_type"].create(
            {
                "name": "Test Tax Validation FPK Type Restricted",
                "code": "/",
                "efaktur_mode": "detail",
                "fpk_journal_selection_method": "domain",
                "fpk_tax_selection_method": "manual",
                "fpk_tax_ids": [(6, 0, [tax_12.id])],
                "tax_id": tax_12.id,
            }
        )
        partner = self.env["res.partner"].create(
            {"name": "Test Tax Validation FPK Partner", "is_company": True}
        )
        # `klikpajak_backend_id` is required once
        # `ssi_l10n_id_taxform_faktur_pajak_klipajak` (a sibling addon in
        # this same repo) is installed -- which `oca_install_addons`
        # always does in CI. `hasattr` keeps this test passing locally
        # too, where that addon is not installed and the field does not
        # exist on the model at all.
        fpk_vals = {
            "type_id": fp_type_restricted.id,
            "tax_id": tax_12.id,
            "partner_id": partner.id,
            "date": "2026-01-15",
            "efaktur_mode": "detail",
        }
        if "klikpajak_backend_id" in self.env["faktur_pajak_keluaran"]._fields:
            klikpajak_backend = self.env["klikpajak_backend"].create(
                {
                    "name": "Test Tax Validation FPK Klikpajak Backend",
                    "code": "/",
                    "base_url": "https://example.test",
                }
            )
            fpk_vals["klikpajak_backend_id"] = klikpajak_backend.id

        fpk = self.env["faktur_pajak_keluaran"].create(fpk_vals)
        self.assertEqual(
            fpk.tax_id,
            tax_12,
            "the allowed header tax must be accepted for the restricted " "type",
        )

        with self.assertRaises(ValidationError):
            fpk.write({"tax_id": tax_11.id})

        self.env["faktur_pajak_keluaran_detail"].create(
            {
                "faktur_pajak_keluaran_id": fpk.id,
                "name": "Test Tax Validation FPK Restricted Line OK",
                "account_id": income_account.id,
                "uom_quantity": 1,
                "price_unit": 1000000.0,
                "tax_ids": [(6, 0, [tax_12.id])],
            }
        )

        with self.assertRaises(ValidationError):
            self.env["faktur_pajak_keluaran_detail"].create(
                {
                    "faktur_pajak_keluaran_id": fpk.id,
                    "name": "Test Tax Validation FPK Restricted Line BAD",
                    "account_id": income_account.id,
                    "uom_quantity": 1,
                    "price_unit": 1000000.0,
                    "tax_ids": [(6, 0, [tax_11.id])],
                }
            )
