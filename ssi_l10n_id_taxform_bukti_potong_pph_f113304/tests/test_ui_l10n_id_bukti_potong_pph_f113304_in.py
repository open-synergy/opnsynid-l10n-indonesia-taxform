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
    "ssi_l10n_id_taxform_bukti_potong_pph_f113304_"
    "l10n_id_bukti_potong_pph_f113304_in_"
)


@tagged("post_install", "-at_install")
class TestUiL10nIdBuktiPotongPphF113304In(HttpSavepointCase):
    """Tour tests for the ``l10n_id.bukti_potong_pph_f113304_in`` work
    instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the master data and documents used by the tours.

        Builds one Pemotong Pajak partner per scenario (so each
        document is identifiable in the list view by its Pemotong
        Pajak column) and one document per state-transition tour, so
        each tour starts from the state its IK Pre-Condition requires.
        """
        super().setUpClass()
        cls.company = cls.env.ref("base.main_company")
        cls.journal = cls.env.ref(
            "ssi_l10n_id_taxform_bukti_potong_pph_f113304.demo_journal1"
        )
        cls.account = cls.env.ref(
            "ssi_l10n_id_taxform_bukti_potong_pph_f113304.demo_account1"
        )
        cls.tax = cls.env.ref("ssi_l10n_id_taxform_bukti_potong_pph_f113304.demo_tax1")
        cls.expense_account = cls.env["account.account"].create(
            {
                "name": "TOUR Expense F113304 In",
                "code": "XTOURF113304IEXP",
                "user_type_id": cls.env.ref(
                    "account.data_account_type_current_liabilities"
                ).id,
                "internal_type": "other",
            }
        )

        cls.tax_period = cls.env["l10n_id.tax_period"].create(
            {
                "name": "TOUR 06/2026 F113304 In",
                "code": "TOUR-06/2026-F113304I",
                "date_start": "2026-06-01",
                "date_end": "2026-06-30",
            }
        )
        cls.kpp = cls.env["res.partner"].create(
            {
                "name": "TOUR KPP F113304 In",
                "is_company": True,
            }
        )

        cls.pemotong_pajak_create = cls._create_pemotong_pajak("TOUR PP CreateF113304I")
        cls.pemotong_pajak_confirm = cls._create_pemotong_pajak(
            "TOUR PP ConfirmF113304I"
        )
        cls.pemotong_pajak_approve = cls._create_pemotong_pajak(
            "TOUR PP ApproveF113304I"
        )
        cls.pemotong_pajak_cancel = cls._create_pemotong_pajak("TOUR PP CancelF113304I")

        # A contact of the "create" scenario's Pemotong Pajak, so it
        # satisfies the TTD field's domain (``commercial_partner_id``
        # equal to the document's Pemotong Pajak).
        cls.ttd = cls.env["res.partner"].create(
            {
                "name": "TOUR TTD F113304 In",
                "is_company": False,
                "parent_id": cls.pemotong_pajak_create.id,
            }
        )

        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR Cancel Reason F113304 In",
                "code": "TOURXF113304I",
                "global_use": True,
            }
        )

        cls.order_confirm = cls._create_order(cls.pemotong_pajak_confirm)
        cls.order_cancel = cls._create_order(cls.pemotong_pajak_cancel)

        # Pre-Condition for the approve tour: on the last approval
        # level, ``action_done`` posts the document's accounting
        # entry (see the "Accounting" tab), which requires at least
        # one withholding line. Build a posted, reconcilable income
        # move line first, so the withholding line has something
        # real to offset when the entry is posted and reconciled.
        cls.order_approve = cls._create_order(cls.pemotong_pajak_approve)
        income_move_line = cls._create_income_move_line(cls.pemotong_pajak_approve)
        cls.env["l10n_id.bukti_potong_pph_f113304_in_line"].create(
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
    def _create_pemotong_pajak(cls, name):
        """Create a partner used to pick from the Pemotong Pajak
        many2one.

        :param name: unique display name of the partner
        :return: the created ``res.partner`` record
        """
        return cls.env["res.partner"].create(
            {
                "name": name,
                "is_company": True,
            }
        )

    @classmethod
    def _create_income_move_line(cls, partner):
        """Create and post a journal entry, then return its debit
        line on ``cls.account``.

        The returned line stands in for the "income" (receivable)
        entry that a withholding line references through
        ``move_line_id``: it must belong to a **posted** move so
        ``_create_aml`` can later reconcile the withholding line's
        credit against it.

        :param partner: partner on the debit line, matching this
            document's Pemotong Pajak (required by the "In"
            direction's allowed move line domain)
        :return: the created ``account.move.line`` (debit side)
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
                            "name": "TOUR Income Line F113304 In",
                            "account_id": cls.account.id,
                            "partner_id": partner.id,
                            "debit": 1000000.0,
                            "credit": 0.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "TOUR Income Line F113304 In Contra",
                            "account_id": cls.expense_account.id,
                            "credit": 1000000.0,
                            "debit": 0.0,
                        },
                    ),
                ],
            }
        )
        move.action_post()
        return move.line_ids.filtered(lambda line: line.debit > 0.0)

    @classmethod
    def _create_order(cls, pemotong_pajak):
        """Create a draft Bukti Potong PPh f.1.1.33.04 In document.

        Leaves ``type_id`` and ``wajib_pajak_id`` unset so their
        field defaults apply, matching what the tour sees after
        opening a new record through the UI.

        :param pemotong_pajak: the ``res.partner`` withholding party
            of the document
        :return: the created ``l10n_id.bukti_potong_pph_f113304_in``
            record
        """
        return cls.env["l10n_id.bukti_potong_pph_f113304_in"].create(
            {
                "tax_period_id": cls.tax_period.id,
                "journal_id": cls.journal.id,
                "account_id": cls.account.id,
                "kpp_id": cls.kpp.id,
                "pemotong_pajak_id": pemotong_pajak.id,
            }
        )

    def test_create(self):
        """Run the create tour for Bukti Potong PPh f.1.1.33.04 In.

        IK: docs/l10n_id_bukti_potong_pph_f113304_in/01-create.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for Bukti Potong PPh f.1.1.33.04 In.

        IK: docs/l10n_id_bukti_potong_pph_f113304_in/04-confirm.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for Bukti Potong PPh f.1.1.33.04 In.

        IK: docs/l10n_id_bukti_potong_pph_f113304_in/05-approve.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "approve",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for Bukti Potong PPh f.1.1.33.04 In.

        IK: docs/l10n_id_bukti_potong_pph_f113304_in/10-cancel.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "cancel",
            login="admin",
        )
