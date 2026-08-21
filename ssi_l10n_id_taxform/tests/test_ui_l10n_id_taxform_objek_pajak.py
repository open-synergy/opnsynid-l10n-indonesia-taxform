# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see skill odoo-development-ui-test, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiL10nIdTaxformObjekPajak(HttpSavepointCase):
    """Tour tests for the ``l10n_id.taxform_objek_pajak`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Grant the configurator group and seed the edit/delete fixtures.

        Pre-Condition common to every ``l10n_id_taxform_objek_pajak`` IK:
        the actor is in group *Objek Pajak*. The group is already
        granted to ``admin`` by this module's own security data
        (``security/res_group_data.xml``); the explicit grant below is
        defensive and mirrors the pattern used by other tour suites in
        this repo family.
        """
        super().setUpClass()
        admin = cls.env.ref("base.user_admin")
        cls.env.ref(
            "ssi_l10n_id_taxform.l10n_id_object_pajak_configurator_group"
        ).sudo().write({"users": [(4, admin.id)]})

        objek_pajak_model = cls.env["l10n_id.taxform_objek_pajak"]

        cls.objek_pajak_edit = objek_pajak_model.create(
            {
                "code": "TOUR-OP-EDIT-01",
                "name": "TOUR-OP-EDIT-UI",
            }
        )
        cls.objek_pajak_delete = objek_pajak_model.create(
            {
                "code": "TOUR-OP-DELETE-01",
                "name": "TOUR-OP-DELETE-UI",
            }
        )

    def test_create(self):
        """Run the create tour for ``l10n_id.taxform_objek_pajak``.

        IK: docs/l10n_id_taxform_objek_pajak/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_l10n_id_taxform_objek_pajak_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``l10n_id.taxform_objek_pajak``.

        IK: docs/l10n_id_taxform_objek_pajak/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_l10n_id_taxform_objek_pajak_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``l10n_id.taxform_objek_pajak``.

        IK: docs/l10n_id_taxform_objek_pajak/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_l10n_id_taxform_objek_pajak_delete",
            login="admin",
        )
