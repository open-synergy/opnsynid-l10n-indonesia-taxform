# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see skill odoo-development-ui-test, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiResPartner(HttpSavepointCase):
    """Tour test for the create-time NITKU field on ``res.partner``."""

    def test_create(self):
        """Run the create tour for ``res.partner``.

        IK: docs/res_partner/01-create.md (E1 delta -- Additional Fields)
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_res_partner_create",
            login="admin",
        )
