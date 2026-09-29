# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestL10nIdTaxformBuktiPotongPphF113301(YamlTransactionCase):
    """YAML-scenario test for Bukti Potong PPh f.1.1.33.01 Out."""

    def test_l10n_id_taxform_bukti_potong_pph_f113301(self):
        """Run the create/confirm/approve/done and policy scenarios.

        Covers the create-and-confirm flow, ``cancel_ok`` restricted
        to state ``done``, ``restart_ok`` allowed on
        ``confirm``/``open``/``reject`` but not on ``cancel``, and the
        positive path of a manual number kept through ``done``. The
        negative path (auto-assigned sequence number unchanged after
        ``done``) is intentionally NOT covered here: this repository
        also ships ``ssi_l10n_id_taxform_coretax_bupot_pph_f113301``,
        which overrides ``_create_sequence_state`` back to ``False``
        on this exact model, so no sequence is ever auto-assigned for
        ``l10n_id.bukti_potong_pph_f113301_out`` once that module is
        installed alongside this one (always true in this repo's CI).
        The equivalent negative-path assertion (``name`` stays ``/``
        through ``done``) already lives in that module's own
        ``test_manual_number_coretax_default.yaml``.
        """
        self.run_yaml_scenario(
            "test_data_l10n_id_taxform_bukti_potong_pph_f113301.yaml"
        )
