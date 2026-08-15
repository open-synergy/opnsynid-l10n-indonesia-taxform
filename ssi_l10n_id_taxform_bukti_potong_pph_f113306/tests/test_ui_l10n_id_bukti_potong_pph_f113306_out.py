# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so tour fixtures would fail with AttributeError.
from odoo.tests import HttpSavepointCase, tagged

#: Common tour name prefix (``<module>_<model>_``), kept as a constant
#: so each ``start_tour()`` call below stays within the line length
#: limit.
_TOUR_PREFIX = (
    "ssi_l10n_id_taxform_bukti_potong_pph_f113306_"
    "l10n_id_bukti_potong_pph_f113306_out_"
)


@tagged("post_install", "-at_install")
class TestUiL10nIdBuktiPotongPphF113306Out(HttpSavepointCase):
    """Tour tests for the ``l10n_id.bukti_potong_pph_f113306_out`` work
    instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the master data and documents used by the tours.

        Builds one taxpayer partner per scenario (so each document is
        identifiable in the list view by its Wajib Pajak column) and
        one document per state-transition tour, so each tour starts
        from the state its IK Pre-Condition requires.
        """
        super().setUpClass()
        cls.company = cls.env.ref("base.main_company")
        cls.journal = cls.env.ref(
            "ssi_l10n_id_taxform_bukti_potong_pph_f113306.demo_journal2"
        )
        cls.account = cls.env.ref(
            "ssi_l10n_id_taxform_bukti_potong_pph_f113306.demo_account3"
        )
        cls.tax = cls.env.ref("ssi_l10n_id_taxform_bukti_potong_pph_f113306.demo_tax2")
        cls.expense_account = cls.env["account.account"].create(
            {
                "name": "TOUR Expense F113306 Out",
                "code": "XTOURF113306OEXP",
                "user_type_id": cls.env.ref(
                    "account.data_account_type_current_liabilities"
                ).id,
                "internal_type": "other",
            }
        )

        cls.tax_period = cls.env["l10n_id.tax_period"].create(
            {
                "name": "TOUR 06/2026 F113306 Out",
                "code": "TOUR-06/2026-F113306O",
                "date_start": "2026-06-01",
                "date_end": "2026-06-30",
            }
        )
        cls.kpp = cls.env["res.partner"].create(
            {
                "name": "TOUR KPP F113306 Out",
                "is_company": True,
            }
        )
        # A contact of the company's partner, so it satisfies the TTD
        # field's domain (``commercial_partner_id`` equal to the
        # document's Pemotong Pajak, which for an "Out" document is
        # automatically the company's own partner).
        cls.ttd = cls.env["res.partner"].create(
            {
                "name": "TOUR TTD F113306 Out",
                "is_company": False,
                "parent_id": cls.company.partner_id.id,
            }
        )

        cls.wajib_pajak_create = cls._create_wajib_pajak("TOUR WP CreateF113306O")
        cls.wajib_pajak_confirm = cls._create_wajib_pajak("TOUR WP ConfirmF113306O")
        cls.wajib_pajak_approve = cls._create_wajib_pajak("TOUR WP ApproveF113306O")
        cls.wajib_pajak_cancel = cls._create_wajib_pajak("TOUR WP CancelF113306O")

        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR Cancel Reason F113306 Out",
                "code": "TOURXF113306O",
                "global_use": True,
            }
        )

        cls.order_confirm = cls._create_order(cls.wajib_pajak_confirm)
        cls.order_cancel = cls._create_order(cls.wajib_pajak_cancel)

        # Pre-Condition for the approve tour: on the last approval
        # level, ``action_done`` posts the document's accounting
        # entry (see the "Accounting" tab), which requires at least
        # one withholding line. Build a posted, reconcilable income
        # move line first, so the withholding line has something
        # real to offset when the entry is posted and reconciled.
        cls.order_approve = cls._create_order(cls.wajib_pajak_approve)
        income_move_line = cls._create_income_move_line(cls.wajib_pajak_approve)
        cls.env["l10n_id.bukti_potong_pph_f113306_out_line"].create(
            {
                "bukti_potong_id": cls.order_approve.id,
                "tax_id": cls.tax.id,
                "move_line_id": income_move_line.id,
                "amount_computation_method": "manual",
                "manual_amount": 1000000.0,
            }
        )
        # Fixture-only transition: bypass the policy check so setup does
        # not depend on the *current* user's group membership — only
        # the tour itself (running as "admin") needs to satisfy the
        # policy.
        cls.order_approve.sudo().with_context(bypass_policy_check=True).action_confirm()

    @classmethod
    def _create_wajib_pajak(cls, name):
        """Create a taxpayer partner used to pick from the Wajib Pajak
        many2one.

        :param name: unique display name of the partner
        :return: the created ``res.partner`` record
        """
        return cls.env["res.partner"].create(
            {
                "name": name,
                "is_company": False,
            }
        )

    @classmethod
    def _create_income_move_line(cls, partner):
        """Create and post a journal entry, then return its credit
        line on ``cls.account``.

        The returned line stands in for the "income" (receivable)
        entry that a withholding line references through
        ``move_line_id``: it must belong to a **posted** move so
        ``_create_aml`` can later reconcile the withholding line's
        debit against it.

        :param partner: partner on the credit line, matching this
            document's Wajib Pajak (required by the "Out" direction's
            allowed move line domain)
        :return: the created ``account.move.line`` (credit side)
        """
        move = cls.env["account.move"].create(
            {
                "journal_id": cls.journal.id,
                "date": "2026-06-15",
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "TOUR Income Line F113306 Out",
                            "account_id": cls.account.id,
                            "partner_id": partner.id,
                            "credit": 1000000.0,
                            "debit": 0.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "TOUR Income Line F113306 Out Contra",
                            "account_id": cls.expense_account.id,
                            "debit": 1000000.0,
                            "credit": 0.0,
                        },
                    ),
                ],
            }
        )
        move.action_post()
        return move.line_ids.filtered(lambda line: line.credit > 0.0)

    @classmethod
    def _create_order(cls, wajib_pajak):
        """Create a draft Bukti Potong PPh f.1.1.33.06 Out document.

        Leaves ``type_id`` and ``pemotong_pajak_id`` unset so their
        field defaults apply, matching what the tour sees after
        opening a new record through the UI.

        :param wajib_pajak: the ``res.partner`` taxpayer of the document
        :return: the created ``l10n_id.bukti_potong_pph_f113306_out``
            record
        """
        return cls.env["l10n_id.bukti_potong_pph_f113306_out"].create(
            {
                "tax_period_id": cls.tax_period.id,
                "journal_id": cls.journal.id,
                "account_id": cls.account.id,
                "kpp_id": cls.kpp.id,
                "wajib_pajak_id": wajib_pajak.id,
                "ttd_id": cls.ttd.id,
            }
        )

    def test_create(self):
        """Run the create tour for Bukti Potong PPh f.1.1.33.06 Out.

        IK: docs/l10n_id_bukti_potong_pph_f113306_out/01-create.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for Bukti Potong PPh f.1.1.33.06 Out.

        IK: docs/l10n_id_bukti_potong_pph_f113306_out/04-confirm.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for Bukti Potong PPh f.1.1.33.06 Out.

        IK: docs/l10n_id_bukti_potong_pph_f113306_out/05-approve.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "approve",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for Bukti Potong PPh f.1.1.33.06 Out.

        IK: docs/l10n_id_bukti_potong_pph_f113306_out/10-cancel.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "cancel",
            login="admin",
        )
