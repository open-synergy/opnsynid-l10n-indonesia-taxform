# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FakturPajakTransactionType(models.Model):
    _name = "l10n_id.faktur_pajak_transaction_type"
    _description = "Faktur Pajak Transaction Type"

    code = fields.Char(
        string="Code",
        required=True,
    )
    name = fields.Char(
        string="Transaction Type",
        required=True,
    )
    description = fields.Text(
        string="Description",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )