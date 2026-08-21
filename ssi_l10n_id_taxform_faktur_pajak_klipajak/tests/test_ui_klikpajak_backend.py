# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, plain HttpCase has no
# cls.env in setUpClass (odoo-development-ui-test structure-and-runner.md
# "Base class").
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiKlikpajakBackend(HttpSavepointCase):
    """UI/UX tour tests for the ``klikpajak_backend`` work instructions.

    Every ``test_*`` method runs the tour paired with the IK file named
    in its docstring (``docs/klikpajak_backend/NN-*.md``). Pre-Condition
    data for those IK files is prepared here in Python, never through
    UI steps, so each tour only walks the click-flow the IK documents.
    """

    @classmethod
    def setUpClass(cls):
        """Create one dedicated backend record per tour.

        ``admin`` already holds ``base.group_system`` (Settings) and,
        through ``base.group_user``, ``base.group_no_one`` (Technical
        Features) via demo data, so no extra group grant is needed for
        the Settings > Technical > Klik Pajak menu to render.

        The restart tour's fixture is created already ``running`` and
        linked to the company, mirroring the real state left behind by
        ``action_running`` -- it is not reached through the running
        tour itself, each tour must stand on its own Pre-Condition.
        """
        super().setUpClass()

        cls.backend_edit = cls._create_backend(
            "TOUR KLIKPAJAK BACKEND Edit",
            parameter_lines=[
                (
                    0,
                    0,
                    {
                        "name": "TOUR_PARAM_EDIT",
                        "type": "char",
                        "value": "old-value",
                    },
                )
            ],
        )
        cls.backend_delete = cls._create_backend("TOUR KLIKPAJAK BACKEND Delete")
        cls.backend_running = cls._create_backend("TOUR KLIKPAJAK BACKEND Running")
        cls.backend_restart = cls._create_backend(
            "TOUR KLIKPAJAK BACKEND Restart", state="running"
        )
        cls.backend_restart.company_id.write(
            {"klikpajak_backend_id": cls.backend_restart.id}
        )

    @classmethod
    def _create_backend(cls, name, state="draft", parameter_lines=None):
        """Create a ``klikpajak_backend`` record for tour Pre-Condition.

        :param str name: Name of the backend record.
        :param str state: Initial ``state`` value.
        :param list parameter_lines: Optional ``(0, 0, {...})`` command
            list for ``parameter_value_ids``.
        :return: The created ``klikpajak_backend`` record.
        :rtype: :class:`odoo.models.Model`
        """
        vals = {
            "name": name,
            "code": "/",
            "base_url": "https://sandbox.klikpajak.id",
            "state": state,
        }
        if parameter_lines:
            vals["parameter_value_ids"] = parameter_lines
        return cls.env["klikpajak_backend"].create(vals)

    def test_create(self):
        """Run the create tour for ``klikpajak_backend``.

        IK: docs/klikpajak_backend/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_faktur_pajak_klipajak_klikpajak_backend_create",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``klikpajak_backend``.

        IK: docs/klikpajak_backend/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_faktur_pajak_klipajak_klikpajak_backend_delete",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``klikpajak_backend``.

        IK: docs/klikpajak_backend/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_faktur_pajak_klipajak_klikpajak_backend_edit",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``klikpajak_backend``.

        IK: docs/klikpajak_backend/05-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_faktur_pajak_klipajak_klikpajak_backend_restart",
            login="admin",
        )

    def test_running(self):
        """Run the running tour for ``klikpajak_backend``.

        IK: docs/klikpajak_backend/04-running.md

        Runs after ``test_restart`` (alphabetical order: "restart" <
        "running"), so ``backend_restart`` is already back to
        ``draft`` by the time this tour's ``action_running`` demotes
        any other running backend of the same company -- there is
        nothing left to demote.
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_faktur_pajak_klipajak_klikpajak_backend_running",
            login="admin",
        )
