# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ResCompany(models.Model):
    """
    Extension point for ``res.company`` reserved for Indonesian tax form
    reporting. This class currently adds no field or method of its own;
    it exists so other modules in this repository can safely extend
    ``res.company`` in the context of ``ssi_l10n_id_taxform`` without
    each redeclaring the inherit chain.
    """

    _name = "res.company"
    _inherit = "res.company"
