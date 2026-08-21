# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see skill odoo-development-ui-test, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiL10nIdTaxYear(HttpSavepointCase):
    """Tour tests for the ``l10n_id.tax_year`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Grant the configurator group and seed one tax year per tour.

        Pre-Condition common to every ``l10n_id_tax_year`` IK: the actor
        is in group *Tax Year* -- without it the Tax Years menu is never
        rendered for "admin" and every tour dies on its first step. The
        group is already granted to ``admin`` by this module's own
        security data (``security/res_group_data.xml``); the explicit
        grant below is defensive and mirrors the pattern used by other
        tour suites in this repo family.
        """
        super().setUpClass()
        cls.env.ref(
            "ssi_l10n_id_taxform.l10n_id_tax_year_configurator_group"
        ).sudo().write({"users": [(4, cls.env.ref("base.user_admin").id)]})

        year_model = cls.env["l10n_id.tax_year"]

        cls.year_edit = year_model.create(
            {
                "name": "TOUR-TY-EDIT-UI",
                "code": "/",
                "date_start": "2028-01-01",
                "date_end": "2028-12-31",
            }
        )
        cls.year_delete = year_model.create(
            {
                "name": "TOUR-TY-DELETE-UI",
                "code": "/",
                "date_start": "2028-01-01",
                "date_end": "2028-12-31",
            }
        )
        cls.year_create_period = year_model.create(
            {
                "name": "TOUR-TY-PERIOD-UI",
                "code": "/",
                "date_start": "2031-01-01",
                "date_end": "2031-12-31",
            }
        )

    def test_create(self):
        """Run the create tour for ``l10n_id.tax_year``.

        IK: docs/l10n_id_tax_year/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_l10n_id_tax_year_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``l10n_id.tax_year``.

        IK: docs/l10n_id_tax_year/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_l10n_id_tax_year_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``l10n_id.tax_year``.

        IK: docs/l10n_id_tax_year/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_l10n_id_tax_year_delete",
            login="admin",
        )

    def test_create_period(self):
        """Run the create-period tour for ``l10n_id.tax_year``.

        IK: docs/l10n_id_tax_year/04-create-period.md
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_l10n_id_tax_year_create_period",
            login="admin",
        )
