# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError

from odoo.addons.ssi_decorator import ssi_decorator


class BuktiPotongPPhf113308Out(models.Model):
    _name = "l10n_id.bukti_potong_pph_f113308_out"
    _inherit = "l10n_id.bukti_potong_pph_mixin"
    _description = "Bukti Potong PPh 26 (f.1.1.33.08) Out"

    def _get_type_id(self):
        type_id = self.env.ref(
            "ssi_l10n_id_taxform_bukti_potong_pph_f113308."
            "bukti_potong_pph_type_f113308_out"
        )
        if not type_id.id:
            err_msg = _("Bukti Potong PPh 26 f113308 Out type hasn't defined")
            raise UserError(err_msg)
        return type_id.id

    @api.model
    def _default_type_id(self):
        return self._get_type_id()

    type_id = fields.Many2one(
        default=lambda self: self._default_type_id(),
    )

    line_ids = fields.One2many(
        comodel_name="l10n_id.bukti_potong_pph_f113308_out_line",
    )

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
