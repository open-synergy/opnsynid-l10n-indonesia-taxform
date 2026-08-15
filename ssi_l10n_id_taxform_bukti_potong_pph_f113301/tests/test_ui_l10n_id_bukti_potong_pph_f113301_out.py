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
    "ssi_l10n_id_taxform_bukti_potong_pph_f113301_"
    "l10n_id_bukti_potong_pph_f113301_out_"
)


@tagged("post_install", "-at_install")
class TestUiL10nIdBuktiPotongPphF113301Out(HttpSavepointCase):
    """Tour tests for the ``l10n_id.bukti_potong_pph_f113301_out`` work
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
            "ssi_l10n_id_taxform_bukti_potong_pph_f113301.demo_journal1"
        )
        cls.account = cls.env.ref(
            "ssi_l10n_id_taxform_bukti_potong_pph_f113301.demo_account1"
        )

        cls.tax_period = cls.env["l10n_id.tax_period"].create(
            {
                "name": "TOUR 06/2026 F113301",
                "code": "TOUR-06/2026-F113301",
                "date_start": "2026-06-01",
                "date_end": "2026-06-30",
            }
        )
        cls.kpp = cls.env["res.partner"].create(
            {
                "name": "TOUR KPP F113301",
                "is_company": True,
            }
        )
        # A contact of the company's partner, so it satisfies the TTD
        # field's domain (``commercial_partner_id`` equal to the
        # document's Pemotong Pajak, which for an "Out" document is
        # automatically the company's own partner).
        cls.ttd = cls.env["res.partner"].create(
            {
                "name": "TOUR TTD F113301",
                "is_company": False,
                "parent_id": cls.company.partner_id.id,
            }
        )

        cls.wajib_pajak_create = cls._create_wajib_pajak("TOUR WP CreateF113301")
        cls.wajib_pajak_confirm = cls._create_wajib_pajak("TOUR WP ConfirmF113301")
        cls.wajib_pajak_approve = cls._create_wajib_pajak("TOUR WP ApproveF113301")
        cls.wajib_pajak_cancel = cls._create_wajib_pajak("TOUR WP CancelF113301")

        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR Cancel Reason F113301",
                "code": "TOURXF113301",
                "global_use": True,
            }
        )

        cls.order_confirm = cls._create_order(cls.wajib_pajak_confirm)
        cls.order_cancel = cls._create_order(cls.wajib_pajak_cancel)

        # Fixture-only transition: bypass the policy check so setup does
        # not depend on the *current* user's group membership — only
        # the tour itself (running as "admin") needs to satisfy the
        # policy.
        cls.order_approve = cls._create_order(cls.wajib_pajak_approve)
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
    def _create_order(cls, wajib_pajak):
        """Create a draft Bukti Potong PPh f.1.1.33.01 Out document.

        Leaves ``type_id`` and ``pemotong_pajak_id`` unset so their
        field defaults apply, matching what the tour sees after
        opening a new record through the UI.

        :param wajib_pajak: the ``res.partner`` taxpayer of the document
        :return: the created ``l10n_id.bukti_potong_pph_f113301_out``
            record
        """
        return cls.env["l10n_id.bukti_potong_pph_f113301_out"].create(
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
        """Run the create tour for Bukti Potong PPh f.1.1.33.01 Out.

        IK: docs/l10n_id_bukti_potong_pph_f113301_out/01-create.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for Bukti Potong PPh f.1.1.33.01 Out.

        IK: docs/l10n_id_bukti_potong_pph_f113301_out/04-confirm.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for Bukti Potong PPh f.1.1.33.01 Out.

        IK: docs/l10n_id_bukti_potong_pph_f113301_out/05-approve.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "approve",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for Bukti Potong PPh f.1.1.33.01 Out.

        IK: docs/l10n_id_bukti_potong_pph_f113301_out/10-cancel.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "cancel",
            login="admin",
        )
