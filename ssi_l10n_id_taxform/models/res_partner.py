# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResPartner(models.Model):
    """
    Adds NITKU tracking to ``res.partner`` for Indonesian tax reporting.

    NITKU (Nomor Induk Tempat Kegiatan Usaha) identifies a taxpayer's
    place of business activity. It is captured on the partner form and
    consumed by other modules in this repository when preparing
    Indonesian tax form documents.
    """

    _inherit = "res.partner"

    nitku = fields.Char(
        string="NITKU",
        help="Nomor Induk Tempat Kegiatan Usaha (NITKU)",
    )
