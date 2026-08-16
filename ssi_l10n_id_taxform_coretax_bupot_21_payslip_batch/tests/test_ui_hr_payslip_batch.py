# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see odoo-development-ui-test skill, structure-and-runner.md
# "Base class").
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrPayslipBatch(HttpSavepointCase):
    """Tour test for the ``hr.payslip_batch`` Export Coretax PPh 21 XML
    button added by this module."""

    @classmethod
    def setUpClass(cls):
        """Drive one batch to ``done`` so the export button is visible.

        Grants ``admin`` the batch and payslip validator groups (needed to
        open/confirm/approve the batch), builds the payroll master data with
        posting accounts, then drives the batch through open, compute,
        confirm and approve with the approval policy bypassed — mirroring
        ``ssi_hr_payroll_batch``'s own journaling test fixture, the only
        proven path to ``done`` in this codebase.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        # Pre-Condition: the batch state buttons/transitions are gated by
        # the batch access groups (open_ok/confirm_ok use the batch User
        # group; approve_ok requires the user to be an approver) and by the
        # payslip Validator group. Granting the batch Validator group
        # implies the batch User group and makes admin an approver on the
        # Standard approval template.
        cls.env.ref(
            "ssi_hr_payroll_batch.hr_payslip_batch_validator_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})
        cls.env.ref("ssi_hr_payroll.hr_payslip_validator_group").sudo().write(
            {"users": [(4, cls.admin.id)]}
        )

        # Pre-Condition master data — posting accounts are required because
        # each payslip creates its own accounting entry when it reaches
        # done (ssi_hr_payroll's hr.payslip._10_create_accounting_entry).
        acc_type = cls.env.ref("account.data_account_type_expenses")
        debit_acc = cls.env["account.account"].create(
            {
                "name": "TOUR Coretax Debit",
                "code": "TOURCTXDB",
                "user_type_id": acc_type.id,
            }
        )
        credit_acc = cls.env["account.account"].create(
            {
                "name": "TOUR Coretax Credit",
                "code": "TOURCTXCR",
                "user_type_id": acc_type.id,
            }
        )
        default_acc = cls.env["account.account"].create(
            {
                "name": "TOUR Coretax Default",
                "code": "TOURCTXDFT",
                "user_type_id": acc_type.id,
            }
        )
        journal = cls.env["account.journal"].create(
            {
                "name": "TOUR Coretax Journal",
                "code": "TCTX",
                "type": "general",
                "default_account_id": default_acc.id,
            }
        )
        rule_category = cls.env["hr.salary_rule_category"].create(
            {"name": "TOUR Coretax Category", "code": "TOURCTXCAT"}
        )
        rule = cls.env["hr.salary_rule"].create(
            {
                "name": "TOUR Coretax Rule",
                "code": "TOURCTXRULE",
                "category_id": rule_category.id,
                "debit_account_id": debit_acc.id,
                "credit_account_id": credit_acc.id,
                "condition_python": "result = True",
                "amount_python": "result = 1000.0",
                "sequence": 10,
            }
        )
        structure = cls.env["hr.salary_structure"].create(
            {
                "name": "TOUR Coretax Structure",
                "code": "TOURCTXSTR",
                "rule_ids": [(4, rule.id)],
            }
        )
        payslip_type = cls.env["hr.payslip_type"].create(
            {
                "name": "TOUR BATCH EXPORT CORETAX",
                "code": "TOURBTCTEC",
                "journal_id": journal.id,
            }
        )
        struct_field = (
            "manual_salary_structure_id"
            if "manual_salary_structure_id" in cls.env["hr.employee"]._fields
            else "salary_structure_id"
        )
        employee = cls.env["hr.employee"].create(
            {
                "name": "TOUR BATCH EXPORT CORETAX EMP",
                struct_field: structure.id,
            }
        )

        # Pre-Condition record: a batch driven to Done as admin, the user
        # the tour logs in as, so the record rule owned by user_id does not
        # hide it from the tour's browser session.
        cls.batch = cls.env["hr.payslip_batch"].create(
            {
                "type_id": payslip_type.id,
                "journal_id": journal.id,
                "date": "2024-01-31",
                "date_start": "2024-01-01",
                "date_end": "2024-01-31",
                "employee_ids": [(6, 0, [employee.id])],
                "user_id": cls.admin.id,
            }
        )
        cls.batch.with_user(cls.admin).action_open()
        cls.batch.invalidate_cache()
        cls.batch.with_user(cls.admin).action_compute_payslip()
        cls.batch.invalidate_cache()
        cls.batch.with_user(cls.admin).with_context(
            bypass_policy_check=True
        ).action_confirm()
        cls.batch.invalidate_cache()
        cls.batch.with_user(cls.admin).with_context(
            bypass_policy_check=True
        ).action_approve_approval()
        cls.batch.invalidate_cache()

    def test_export_coretax(self):
        """Run the Export Coretax PPh 21 XML tour for ``hr.payslip_batch``.

        IK: docs/hr_payslip_batch/20-export-coretax.md
        """
        self.start_tour(
            "/web",
            # noqa: B950 — tour name follows the mandatory
            # <module>_<model>_<action> prefix convention.
            "ssi_l10n_id_taxform_coretax_bupot_21_payslip_batch_hr_payslip_batch_export_coretax",  # noqa: B950
            login="admin",
        )
