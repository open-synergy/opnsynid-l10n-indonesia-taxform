# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so tour fixtures would fail with AttributeError.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiL10nIdBuktiPotongPphF113301Out(HttpSavepointCase):
    """Tour test for the Coretax "input Coretax number" work
    instruction added by this module."""

    @classmethod
    def setUpClass(cls):
        """Create one Bukti Potong PPh f.1.1.33.01 Out document already
        Waiting for Approval, so the tour starts from the state its IK
        Pre-Condition requires.
        """
        super().setUpClass()
        cls.tax_period = cls.env["l10n_id.tax_period"].create(
            {
                "name": "TOUR 06/2026 Input Nomor Coretax F113301",
                "code": "TOUR-06/2026-INC-F113301",
                "date_start": "2026-06-01",
                "date_end": "2026-06-30",
            }
        )
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "TOUR Journal Input Nomor Coretax F113301",
                "code": "TJINCF113301",
                "type": "general",
            }
        )
        cls.account = cls.env["account.account"].create(
            {
                "name": "TOUR Account Input Nomor Coretax F113301",
                "code": "XTOURINCF113301",
                "user_type_id": cls.env.ref(
                    "account.data_account_type_current_liabilities"
                ).id,
                "internal_type": "other",
            }
        )
        cls.kpp = cls.env["res.partner"].create(
            {
                "name": "TOUR KPP Input Nomor Coretax F113301",
                "is_company": True,
            }
        )
        cls.wajib_pajak = cls.env["res.partner"].create(
            {
                "name": "TOUR WP InputNomorCoretaxF113301",
                "is_company": False,
            }
        )
        # A contact of the company's partner, so it satisfies the TTD
        # field's domain (``commercial_partner_id`` equal to the
        # document's Pemotong Pajak, which for an "Out" document is
        # automatically the company's own partner).
        cls.ttd = cls.env["res.partner"].create(
            {
                "name": "TOUR TTD Input Nomor Coretax F113301",
                "is_company": False,
                "parent_id": cls.env.ref("base.main_company").partner_id.id,
            }
        )

        cls.order = cls.env["l10n_id.bukti_potong_pph_f113301_out"].create(
            {
                "tax_period_id": cls.tax_period.id,
                "journal_id": cls.journal.id,
                "account_id": cls.account.id,
                "kpp_id": cls.kpp.id,
                "wajib_pajak_id": cls.wajib_pajak.id,
                "ttd_id": cls.ttd.id,
            }
        )
        # Fixture-only transition: bypass the policy check so setup
        # does not depend on the *current* user's group membership —
        # only the tour itself (running as "admin") needs to satisfy
        # the policy.
        cls.order.sudo().with_context(bypass_policy_check=True).action_confirm()

    def test_input_nomor_coretax(self):
        """Run the "input Coretax number" tour for Bukti Potong PPh
        f.1.1.33.01 Out.

        IK: docs/l10n_id_bukti_potong_pph_f113301_out/
        07-input-nomor-coretax.md
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_coretax_bupot_pph_f113301_"
            "l10n_id_bukti_potong_pph_f113301_out_input_nomor_coretax",
            login="admin",
        )
