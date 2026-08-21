# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see skill odoo-development-ui-test, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiL10nIdTaxPeriod(HttpSavepointCase):
    """Tour tests for the ``l10n_id.tax_period`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Grant the configurator groups and seed the period fixtures.

        Pre-Condition common to every ``l10n_id_tax_period`` IK: the
        actor is in group *Tax Period*, and an ``l10n_id.tax_year``
        record exists for the period to link to (see
        ``docs/l10n_id_tax_period/01-create.md``). Both configurator
        groups are already granted to ``admin`` by this module's own
        security data (``security/res_group_data.xml``); the explicit
        grants below are defensive and mirror the pattern used by other
        tour suites in this repo family.
        """
        super().setUpClass()
        admin = cls.env.ref("base.user_admin")
        cls.env.ref(
            "ssi_l10n_id_taxform.l10n_id_tax_year_configurator_group"
        ).sudo().write({"users": [(4, admin.id)]})
        cls.env.ref(
            "ssi_l10n_id_taxform.l10n_id_tax_period_configurator_group"
        ).sudo().write({"users": [(4, admin.id)]})

        cls.year = cls.env["l10n_id.tax_year"].create(
            {
                "name": "TOUR-TP-YEAR-UI",
                "code": "/",
                "date_start": "2029-01-01",
                "date_end": "2029-12-31",
            }
        )

        period_model = cls.env["l10n_id.tax_period"]

        cls.period_edit = period_model.create(
            {
                "name": "TOUR-TP-EDIT-UI",
                "code": "/",
                "year_id": cls.year.id,
                "date_start": "2029-01-01",
                "date_end": "2029-01-31",
            }
        )
        cls.period_delete = period_model.create(
            {
                "name": "TOUR-TP-DELETE-UI",
                "code": "/",
                "year_id": cls.year.id,
                "date_start": "2029-02-01",
                "date_end": "2029-02-28",
            }
        )

    def test_create(self):
        """Run the create tour for ``l10n_id.tax_period``.

        IK: docs/l10n_id_tax_period/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_l10n_id_tax_period_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``l10n_id.tax_period``.

        IK: docs/l10n_id_tax_period/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_l10n_id_tax_period_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``l10n_id.tax_period``.

        IK: docs/l10n_id_tax_period/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_l10n_id_tax_period_delete",
            login="admin",
        )
