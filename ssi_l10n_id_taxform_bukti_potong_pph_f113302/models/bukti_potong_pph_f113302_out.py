# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError


class BuktiPotongPPhf113302Out(models.Model):
    _name = "l10n_id.bukti_potong_pph_f113302_out"
    _inherit = "l10n_id.bukti_potong_pph_mixin"
    _description = "Bukti Potong PPh 21 Final (f.1.1.33.02) Out"

    def _get_type_id(self):
        type_id = self.env.ref(
            "ssi_l10n_id_taxform_bukti_potong_pph_f113302."
            "bukti_potong_pph_type_f113302_out"
        )
        if not type_id.id:
            err_msg = _("Bukti Potong PPh 21 Final f113302 Out type hasn't defined")
            raise UserError(err_msg)
        return type_id.id

    @api.model
    def _default_type_id(self):
        return self._get_type_id()

    type_id = fields.Many2one(
        default=lambda self: self._default_type_id(),
    )

    line_ids = fields.One2many(
        comodel_name="l10n_id.bukti_potong_pph_f113302_out_line",
    )
