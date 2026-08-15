# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so the tour fixtures below would fail with
# AttributeError.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiL10nIdBuktiPotongPphF113304OutOperatingUnit(HttpSavepointCase):
    """UI/UX tour test for the Operating Unit field this module adds to
    ``l10n_id.bukti_potong_pph_f113304_out`` (E1 delta -- Additional
    Fields).

    Pairs with IK ``docs/l10n_id_bukti_potong_pph_f113304_out/
    01-create.md`` (delta), backed by the base IK
    ``ssi_l10n_id_taxform_bukti_potong_pph_f113304/docs/
    l10n_id_bukti_potong_pph_f113304_out/01-create.md`` for the
    navigation up to the New button.
    """

    @classmethod
    def setUpClass(cls):
        """Put the tour user in the multi operating unit group.

        The Operating Unit field is gated by the multi operating unit
        group (``groups="operating_unit.group_multi_operating_unit"``
        in the view) -- without it, the field is never rendered and
        the delta assertion would never find it. The user also needs
        at least one operating unit assigned so the field has a
        meaningful (non-empty) allowed set.
        """
        super().setUpClass()
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.operating_unit_partner = cls.env["res.partner"].create(
            {"name": "TOUR Bukti Potong F113304 Out OU Partner"}
        )
        cls.operating_unit = cls.env["operating.unit"].create(
            {
                "name": "TOUR Bukti Potong F113304 Out Operating Unit",
                "code": "TBP304OOU",
                "partner_id": cls.operating_unit_partner.id,
            }
        )
        cls.env.ref("operating_unit.group_multi_operating_unit").sudo().write(
            {"users": [(4, cls.user_admin.id)]}
        )
        cls.user_admin.sudo().write(
            {
                "assigned_operating_unit_ids": [(4, cls.operating_unit.id)],
                "default_operating_unit_id": cls.operating_unit.id,
            }
        )

    def test_field_operating_unit(self):
        """Run the create tour, asserting the Operating Unit field.

        IK: docs/l10n_id_bukti_potong_pph_f113304_out/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_l10n_id_taxform_bukti_potong_pph_f113304_operating_unit"
            "_l10n_id_bukti_potong_pph_f113304_out_create",
            login="admin",
        )
