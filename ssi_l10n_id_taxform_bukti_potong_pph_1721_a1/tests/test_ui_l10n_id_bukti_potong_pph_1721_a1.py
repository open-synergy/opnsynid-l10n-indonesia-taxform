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
    "ssi_l10n_id_taxform_bukti_potong_pph_1721_a1_" "l10n_id_bukti_potong_pph_1721_a1_"
)


@tagged("post_install", "-at_install")
class TestUiL10nIdBuktiPotongPph1721A1(HttpSavepointCase):
    """Tour tests for the ``l10n_id.bukti_potong_pph_1721_a1`` work
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
        cls.admin = cls.env.ref("base.user_admin")
        cls.company = cls.env.ref("base.main_company")

        cls.ptkp_category = cls.env.ref("ssi_l10n_id_taxform_pph_21.ptkp_tk0")
        cls.objek_pajak = cls.env.ref(
            "ssi_l10n_id_taxform.l10n_id_taxform_objek_pajak_21_100_01"
        )
        cls.tax_period = cls.env["l10n_id.tax_period"].create(
            {
                "name": "TOUR 01/2026",
                "code": "TOUR-01/2026",
                "date_start": "2026-01-01",
                "date_end": "2026-01-31",
            }
        )

        cls.wajib_pajak_create = cls._create_wajib_pajak("TOUR WP Create1721A1")
        cls.wajib_pajak_edit_source = cls._create_wajib_pajak(
            "TOUR WP EditSource1721A1"
        )
        cls.wajib_pajak_edit_target = cls._create_wajib_pajak(
            "TOUR WP EditTarget1721A1"
        )
        cls.wajib_pajak_delete = cls._create_wajib_pajak("TOUR WP Delete1721A1")
        cls.wajib_pajak_confirm = cls._create_wajib_pajak("TOUR WP Confirm1721A1")
        cls.wajib_pajak_approve = cls._create_wajib_pajak("TOUR WP Approve1721A1")
        cls.wajib_pajak_reject = cls._create_wajib_pajak("TOUR WP Reject1721A1")
        cls.wajib_pajak_cancel = cls._create_wajib_pajak("TOUR WP Cancel1721A1")
        cls.wajib_pajak_restart = cls._create_wajib_pajak("TOUR WP Restart1721A1")
        cls.wajib_pajak_restart_approval = cls._create_wajib_pajak(
            "TOUR WP RestartAppr1721A1"
        )

        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR Cancel Reason 1721A1",
                "code": "TOURX1721A1",
                "global_use": True,
            }
        )

        cls.order_edit = cls._create_order(cls.wajib_pajak_edit_source)
        cls.order_delete = cls._create_order(cls.wajib_pajak_delete)
        cls.order_confirm = cls._create_order(cls.wajib_pajak_confirm)

        # Fixture-only transitions: bypass the policy check so setup does
        # not depend on the *current* user's group membership — only the
        # tour itself (running as "admin") needs to satisfy the policy.
        cls.order_approve = cls._create_order(cls.wajib_pajak_approve)
        cls.order_approve.sudo().with_context(bypass_policy_check=True).action_confirm()

        cls.order_reject = cls._create_order(cls.wajib_pajak_reject)
        cls.order_reject.sudo().with_context(bypass_policy_check=True).action_confirm()

        cls.order_cancel = cls._create_order(cls.wajib_pajak_cancel)

        cls.order_restart = cls._create_order(cls.wajib_pajak_restart)
        cls.order_restart.sudo().write({"state": "cancel"})

        cls.order_restart_approval = cls._create_order(cls.wajib_pajak_restart_approval)
        cls.order_restart_approval.sudo().with_context(
            bypass_policy_check=True
        ).action_confirm()
        # Pre-Condition for "Restart Approval Process": the approval
        # template got detached from the record while it is still
        # waiting for approval (see policy_template_data.xml).
        cls.order_restart_approval.sudo().approval_template_id = False

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
                "ektp_number": "3201010101900001",
                "vat": "01.234.567.8-901.000",
                "street": "Jl. Tour Test No. 1",
                "city": "Jakarta",
                "zip": "12345",
                "function": "Staff",
                "ptkp_category_id": cls.ptkp_category.id,
            }
        )

    @classmethod
    def _create_order(cls, wajib_pajak):
        """Create a draft Form 1721 A1 document for ``wajib_pajak``.

        Fills the identity fields directly instead of relying on
        ``onchange_wajib_pajak_id`` (ORM ``create()`` does not trigger
        onchange), matching what the tour later sees after step 3 of
        ``01-create.md`` fills them through the UI.

        :param wajib_pajak: the ``res.partner`` taxpayer of the document
        :return: the created ``l10n_id.bukti_potong_pph_1721_a1`` record
        """
        return cls.env["l10n_id.bukti_potong_pph_1721_a1"].create(
            {
                "wajib_pajak_id": wajib_pajak.id,
                "wajib_pajak_npwp": wajib_pajak.vat,
                "wajib_pajak_alamat": wajib_pajak.street,
                "wajib_pajak_nik": wajib_pajak.ektp_number,
                "wajib_pajak_ptkp_category_id": cls.ptkp_category.id,
                "wajib_pajak_job_position": wajib_pajak.function,
                "kode_objek_pajak_id": cls.objek_pajak.id,
                "start_tax_period_id": cls.tax_period.id,
                "end_tax_period_id": cls.tax_period.id,
            }
        )

    def test_create(self):
        """Run the create tour for Form 1721 A1.

        IK: docs/l10n_id_bukti_potong_pph_1721_a1/01-create.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for Form 1721 A1.

        IK: docs/l10n_id_bukti_potong_pph_1721_a1/02-edit.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for Form 1721 A1.

        IK: docs/l10n_id_bukti_potong_pph_1721_a1/03-delete.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for Form 1721 A1.

        IK: docs/l10n_id_bukti_potong_pph_1721_a1/04-confirm.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for Form 1721 A1.

        IK: docs/l10n_id_bukti_potong_pph_1721_a1/05-approve.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for Form 1721 A1.

        IK: docs/l10n_id_bukti_potong_pph_1721_a1/06-reject.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "reject",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for Form 1721 A1.

        IK: docs/l10n_id_bukti_potong_pph_1721_a1/10-cancel.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for Form 1721 A1.

        IK: docs/l10n_id_bukti_potong_pph_1721_a1/12-restart.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "restart",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval process tour for Form 1721 A1.

        IK: docs/l10n_id_bukti_potong_pph_1721_a1/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            _TOUR_PREFIX + "restart_approval",
            login="admin",
        )
