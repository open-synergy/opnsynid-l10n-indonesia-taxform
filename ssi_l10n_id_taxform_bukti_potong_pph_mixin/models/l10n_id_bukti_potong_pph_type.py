# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class L10nIdBuktiPotongPphType(models.Model):
    """Master data of Bukti Potong PPh types (form types).

    Each record represents one Indonesian withholding tax slip (Bukti
    Potong PPh) form type, such as f.1.1.33.01 or f.1.1.33.10. It
    restricts which journal, tax, and account are allowed to be used
    on documents created with this type. Concrete downstream modules
    (one per form type) each own a single fixed record of this model
    and expose it through their own configuration menu.
    """

    _name = "l10n_id.bukti_potong_pph_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Type of Bukti Potong PPh"

    name = fields.Char(
        string="Type",
        required=True,
        translate=True,
    )
    direction = fields.Selection(
        string="Direction",
        selection=[
            ("in", "In"),
            ("out", "Out"),
        ],
        required=True,
    )
    journal_ids = fields.Many2many(
        string="Allowed Journals",
        comodel_name="account.journal",
        relation="rel_bukpot_pph_type_2_journal",
        column1="type_id",
        column2="journal_id",
    )
    tax_ids = fields.Many2many(
        string="Allowed Taxes",
        comodel_name="account.tax",
        relation="rel_bukpot_type_2_tax",
        column1="type_id",
        column2="tax_id",
    )
    account_ids = fields.Many2many(
        string="Allowed Accounts",
        comodel_name="account.account",
        relation="rel_bukpot_type_2_account",
        column1="type_id",
        column2="account_id",
    )
