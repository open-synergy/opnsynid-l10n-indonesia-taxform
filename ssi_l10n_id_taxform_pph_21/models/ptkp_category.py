# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import models


class PtkpCategory(models.Model):
    _name = "l10n_id.ptkp_category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Kategori PTKP"

    def get_rate(self, dt=None):
        self.ensure_one()
        obj_ptkp = self.env["l10n_id.ptkp"]
        ptkp = obj_ptkp.find(dt)
        result = ptkp.get_rate(self)
        return result
