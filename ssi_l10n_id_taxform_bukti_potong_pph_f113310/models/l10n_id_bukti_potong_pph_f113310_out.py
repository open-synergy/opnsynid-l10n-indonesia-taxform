# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError

from odoo.addons.ssi_decorator import ssi_decorator


class L10nIdBuktiPotongPphF113310Out(models.Model):
    """Indonesia's PPh 4(2) outgoing withholding slip, form f.1.1.33.10.

    Records outgoing (company-issued) tax withholding through the
    standard confirm/approve/done workflow, then generates the related
    journal entry once the document is done.
    """

    _name = "l10n_id.bukti_potong_pph_f113310_out"
    _inherit = "l10n_id.bukti_potong_pph_mixin"
    _description = "Bukti Potong PPh 4(2) f.1.1.33.10 Out"

    def _get_type_id(self):
        """Look up this module's ``l10n_id.bukti_potong_pph_type`` record.

        :return: id of the "f113310 Out" form type
        :raises UserError: when the type record has not been loaded
        """
        type_id = self.env.ref(
            "ssi_l10n_id_taxform_bukti_potong_pph_f113310."
            "bukti_potong_pph_type_f113310_out"
        )
        if not type_id.id:
            err_msg = _("Bukti Potong PPh 4(2) f113310 Out type hasn't defined")
            raise UserError(err_msg)
        return type_id.id

    @api.model
    def _default_type_id(self):
        """Return the default ``type_id`` value.

        :return: id of the "f113310 Out" form type
        """
        return self._get_type_id()

    type_id = fields.Many2one(
        default=lambda self: self._default_type_id(),
    )

    line_ids = fields.One2many(
        comodel_name="l10n_id.bukti_potong_pph_f113310_out_line",
    )

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
