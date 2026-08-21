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
        # `_compute_taxform_period` calls `l10n_id.tax_period._find_period`
        # on every create, which raises if no period covers the date. Our
        # local `devel` DB is a production-like restore with periods for
        # almost every date, which masked this; CI's clean test DB has
        # none, so it is created explicitly here for every environment.
        self.env["l10n_id.tax_period"].create(
            {
                "name": "Test Tax Validation FPK Period 01/2026",
                "code": "/",
                "date_start": "2026-01-01",
                "date_end": "2026-01-31",
            }
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

    def test_price_unit_gross_up_for_non_percent_include_tax(self):
        """Gross-up must not assume `percent`, only `price_include`.

        Reproduces a bug found via the SGRS production server: FPK
        ID=14 / invoice CLM/2607/001. After the first fix for this
        module (grossing up `price_unit` when a detail line's tax is
        Include) shipped, the tax "PPN Keluaran 11% (Include)" was
        reconfigured on that server from `amount_type: percent` to a
        custom `python_compute` ("code") formula -- mathematically the
        same 11% Include tax, just no longer reachable through
        `tax.amount`/`tax.amount_type == "percent"`. The fix was
        changed to numerically invert `account.tax.compute_all`
        instead of assuming a formula, so it works for any Include tax.

        This test exercises that against Odoo's own core `division`
        tax type ("Percentage of Price Tax Included") rather than a
        `python_compute` tax matching the SGRS config exactly: the
        `python_compute`/`amount_type: code` fields only exist once an
        extra addon is installed that is not part of this repo's
        `oca_install_addons`-resolved dependency set, so a test tax
        using them fails in CI with "Invalid field 'python_compute' on
        model 'account.tax'" (confirmed by a CI run that hit exactly
        this). `division` is a plain `account` core feature, genuinely
        not `percent`, which is the property under test here.

        Trigger/limitation: P2, L-04 -- `division` computes
        `price_tax` as a division rather than a simple percentage
        multiplication, so `compute_all`'s float result does not
        round-trip to the literal `123595.51` bit-for-bit (it comes
        back as `123595.51000000001`); YAML's `equals` assert is a raw
        `!=` with no tolerance, so this cannot be expressed as YAML.
        """
        revenue_type = self.env.ref("account.data_account_type_revenue")
        liability_type = self.env.ref("account.data_account_type_current_liabilities")
        income_account = self.env["account.account"].create(
            {
                "code": "FPKDIV1",
                "name": "Test Division Tax FPK Income",
                "user_type_id": revenue_type.id,
            }
        )
        tax_account = self.env["account.account"].create(
            {
                "code": "FPKDIV2",
                "name": "Test Division Tax FPK VAT Payable",
                "user_type_id": liability_type.id,
            }
        )
        division_tax = self.env["account.tax"].create(
            {
                "name": "Test Division Tax FPK VAT 11pct Include",
                "amount_type": "division",
                "amount": 11.0,
                "type_tax_use": "sale",
                "price_include": True,
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
        fp_type = self.env["faktur_pajak_transaction_type"].create(
            {
                "name": "Test Division Tax FPK Type",
                "code": "/",
                "efaktur_mode": "detail",
                "fpk_journal_selection_method": "domain",
                "fpk_tax_selection_method": "manual",
                "fpk_tax_ids": [(6, 0, [division_tax.id])],
                "tax_id": division_tax.id,
            }
        )
        partner = self.env["res.partner"].create(
            {"name": "Test Division Tax FPK Partner", "is_company": True}
        )
        self.env["l10n_id.tax_period"].create(
            {
                "name": "Test Division Tax FPK Period 01/2026",
                "code": "/",
                "date_start": "2026-01-01",
                "date_end": "2026-01-31",
            }
        )
        fpk_vals = {
            "type_id": fp_type.id,
            "tax_id": division_tax.id,
            "partner_id": partner.id,
            "date": "2026-01-15",
            "efaktur_mode": "detail",
        }
        if "klikpajak_backend_id" in self.env["faktur_pajak_keluaran"]._fields:
            klikpajak_backend = self.env["klikpajak_backend"].create(
                {
                    "name": "Test Division Tax FPK Klikpajak Backend",
                    "code": "/",
                    "base_url": "https://example.test",
                }
            )
            fpk_vals["klikpajak_backend_id"] = klikpajak_backend.id
        fpk = self.env["faktur_pajak_keluaran"].create(fpk_vals)

        base_amount = 1000000.0
        detail = self.env["faktur_pajak_keluaran_detail"].create(
            {
                "faktur_pajak_keluaran_id": fpk.id,
                "name": "Test Division Tax FPK Line",
                "account_id": income_account.id,
                "uom_quantity": 1,
                "price_unit": base_amount,
                "base_amount": base_amount,
                "tax_ids": [(6, 0, [division_tax.id])],
            }
        )

        fpk.action_compute_tax()
        detail.invalidate_cache()

        self.assertAlmostEqual(
            detail.price_subtotal,
            base_amount,
            places=2,
            msg="DPP must stay anchored to base_amount for a non-percent "
            "Include tax, not just plain percent taxes",
        )
        self.assertAlmostEqual(
            detail.price_unit,
            1123595.51,
            places=2,
            msg="price_unit must be grossed up correctly for the division tax",
        )
        self.assertAlmostEqual(
            detail.price_tax,
            123595.51,
            places=2,
            msg="PPN must be computed from the correct (ungrossed) DPP",
        )
