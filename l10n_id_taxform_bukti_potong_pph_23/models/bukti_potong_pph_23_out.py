# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class BuktiPotongPPh23Out(models.Model):
    _name = "l10n_id.bukti_potong_pph_23_out"
    _inherit = "l10n_id.bukti_potong_pph"
    _table = "l10n_id_bukti_potong_pph"
    _description = "Bukti Potong PPh 23 Out"

    @api.model
    def _default_type_id(self):
        return self.env.ref(
            "l10n_id_taxform_bukti_potong_pph_23."
            "bukti_potong_pph_type_f113306_out").id

    type_id = fields.Many2one(
        default=lambda self: self._default_type_id(),
    )

    @api.model
    def search(self, args, offset=0, limit=None, order=None):
        type_id = self.env.ref(
            "l10n_id_taxform_bukti_potong_pph_23."
            "bukti_potong_pph_type_f113306_out")
        args.append(("type_id", "=", type_id.id))
        return super(BuktiPotongPPh23Out, self).\
            search(args, offset, limit, order)
