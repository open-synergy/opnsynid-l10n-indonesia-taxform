# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see odoo-development-ui-test skill, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiL10nIdBuktiPotongPphF113306Out(HttpSavepointCase):
    """Tour test for the create-time Work Log page.

    No fixture data is needed: this model's ``validator_group`` and
    ``all_group`` already grant ``base.user_admin`` membership by
    default (see the base module's ``security/res_group_data.xml``),
    so ``admin`` can open the **New** form without any extra setup,
    and the delta being tested is visible on that unsaved form.
    """

    def test_create(self):
        """Run the create tour for ``l10n_id.bukti_potong_pph_f113306_out``.

        IK: docs/l10n_id_bukti_potong_pph_f113306_out/01-create.md (E2a
        delta -- Modified Flow)
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_bukti_potong_pph_f113306_work_log_"
            "l10n_id_bukti_potong_pph_f113306_out_create",
            login="admin",
        )
