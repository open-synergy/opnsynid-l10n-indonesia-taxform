# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass (see odoo-development-ui-test skill,
# structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiL10nIdBuktiPotongPphF113301Out(HttpSavepointCase):
    """Tour test for the Work Log page on Create."""

    @classmethod
    def setUpClass(cls):
        """Create the master data used to fill the create form.

        Mirrors the master data set up by the base module's own
        create tour (see
        ``ssi_l10n_id_taxform_bukti_potong_pph_f113301``'s
        ``test_ui_l10n_id_bukti_potong_pph_f113301_out.py``), reusing
        its ``demo_journal1``/``demo_account1`` demo records so the
        journal/account labels asserted by the tour match existing
        data. Only a Draft-state fixture is needed here -- this tour
        asserts a newly created record, not a state transition.
        """
        super().setUpClass()
        cls.journal = cls.env.ref(
            "ssi_l10n_id_taxform_bukti_potong_pph_f113301.demo_journal1"
        )
        cls.account = cls.env.ref(
            "ssi_l10n_id_taxform_bukti_potong_pph_f113301.demo_account1"
        )
        cls.tax_period = cls.env["l10n_id.tax_period"].create(
            {
                "name": "TOUR 06/2026 F113301WL",
                "code": "TOUR-06/2026-F113301WL",
                "date_start": "2026-06-01",
                "date_end": "2026-06-30",
            }
        )
        cls.kpp = cls.env["res.partner"].create(
            {
                "name": "TOUR KPP F113301WL",
                "is_company": True,
            }
        )
        # A contact of the company's partner, so it satisfies the TTD
        # field's domain (``commercial_partner_id`` equal to the
        # document's Pemotong Pajak, which for an "Out" document is
        # automatically the company's own partner).
        cls.ttd = cls.env["res.partner"].create(
            {
                "name": "TOUR TTD F113301WL",
                "is_company": False,
                "parent_id": cls.env.company.partner_id.id,
            }
        )
        cls.wajib_pajak = cls.env["res.partner"].create(
            {
                "name": "TOUR WP CreateF113301WL",
                "is_company": False,
            }
        )

    def test_create(self):
        """Run the create tour for the f.1.1.33.01 Out model.

        IK: docs/l10n_id_bukti_potong_pph_f113301_out/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_bukti_potong_pph_f113301_work_log_"
            "l10n_id_bukti_potong_pph_f113301_out_create",
            login="admin",
        )
