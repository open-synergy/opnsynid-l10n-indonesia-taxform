# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAmountTaxDppRate(YamlTransactionCase):
    """Scenario tests for ``amount_tax`` computed from ``dpp`` x ``rate``.

    Covers the BP21 f.1.1.33.01 Out line override that derives
    ``amount_tax`` from this line's own ``dpp``/``rate`` instead of
    ``tax_id.compute_all()``, so a ``tax_id`` deliberately set to 0%
    (to avoid double-counting a rate already captured by ``dpp``/
    ``rate``) no longer forces ``amount_tax`` to 0 — and the fallback
    to ``tax_id.compute_all()`` that still applies to lines whose
    ``dpp``/``rate`` were never configured (pre-existing lines from
    ``ssi_l10n_id_taxform_bukti_potong_pph_f113301``).
    """

    def test_amount_tax_from_dpp_rate(self):
        """``amount_tax`` follows ``dpp`` x ``rate`` and stays in sync
        after ``manual_rate`` is written."""
        self.run_yaml_scenario("test_amount_tax_from_dpp_rate.yaml")

    def test_amount_tax_zero_rate_rejected(self):
        """A line with ``manual_rate = 0.0`` still yields
        ``amount_tax == 0.0`` and is rejected by
        ``_constrains_total_tax_final`` (existing behaviour,
        unchanged by the ``dpp`` x ``rate`` override)."""
        self.run_yaml_scenario("test_amount_tax_zero_rate_rejected.yaml")

    def test_amount_tax_fallback_tax_id(self):
        """A line that never went through the Coretax rate
        configuration (``rate`` left at its default ``0.0``, as on
        pre-existing ``ssi_l10n_id_taxform_bukti_potong_pph_f113301``
        lines) still gets ``amount_tax`` from ``tax_id.compute_all()``,
        exactly as before this module's ``dpp`` x ``rate`` override
        existed."""
        self.run_yaml_scenario("test_amount_tax_fallback_tax_id.yaml")
