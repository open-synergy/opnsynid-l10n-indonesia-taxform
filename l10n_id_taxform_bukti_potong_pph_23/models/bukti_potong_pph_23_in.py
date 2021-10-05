# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class BuktiPotongPPh23In(models.Model):
    _name = "l10n_id.bukti_potong_pph_23_in"
    _inherit = "l10n_id.bukti_potong_pph"
    _table = "l10n_id_bukti_potong_pph"
    _description = "Bukti Potong PPh 23 In"

    @api.multi
    def _get_type_id(self):
        self.ensure_one()
        type_id = self.env.ref(
            "l10n_id_taxform_bukti_potong_pph_23." "bukti_potong_pph_type_f113306_in"
        )
        if not type_id.id:
            err_msg = _("Bukti Potong PPh 23 In type hasn't defined")
            raise UserError(err_msg)
        return type_id.id

    @api.model
    def _default_type_id(self):
        return self._get_type_id()

    type_id = fields.Many2one(
        default=lambda self: self._default_type_id(),
    )

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        type_id = self._get_type_id()
        args.append(("type_id", "=", type_id))
        return super(BuktiPotongPPh23In, self).search(
            args=args, offset=offset, limit=limit, order=order, count=count
        )
