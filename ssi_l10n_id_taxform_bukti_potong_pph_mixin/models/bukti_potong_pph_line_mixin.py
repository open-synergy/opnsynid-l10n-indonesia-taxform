# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.tools.translate import _


class BuktiPotongPPhLineMixin(models.AbstractModel):
    _name = "l10n_id.bukti_potong_pph_line_mixin"
    _description = "Bukti Potong PPh Line Mixin"
    _order = "sequence, id"

    @api.depends(
        "income_move_line_ids",
        "income_move_line_ids.debit",
        "income_move_line_ids.credit",
    )
    def _compute_amount(self):
        for line in self:
            line.amount = 0.0
            for move_line in line.income_move_line_ids:
                if line.bukti_potong_id.direction == "in":
                    line.amount += move_line.credit
                else:
                    line.amount += move_line.debit
            if line.amount != 0.0:
                taxes = line.tax_id.compute_all(
                    line.amount,
                    line.bukti_potong_id.company_id.currency_id,
                    1.0,
                    product=False,
                    partner=False,
                )
                line.amount_tax = taxes["total_included"] - taxes["total_excluded"]

    name = fields.Char(
        string="Description",
        required=True,
        default="/",
    )
    bukti_potong_id = fields.Many2one(
        string="Bukti Potong",
        comodel_name="l10n_id.bukti_potong_pph_mixin",
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    tax_id = fields.Many2one(
        string="Tax",
        comodel_name="account.tax",
        required=True,
        ondelete="restrict",
    )
    move_line_id = fields.Many2one(
        string="Move Line",
        comodel_name="account.move.line",
        copy=False,
        ondelete="restrict",
    )
    income_move_line_ids = fields.Many2many(
        string="Income Move Lines",
        comodel_name="account.move.line",
        relation="rel_bukpot_line_2_income_move",
        column1="bukpot_line_id",
        column2="account_move_id",
    )
    amount = fields.Float(
        string="Amount",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
    )
    amount_tax = fields.Float(
        string="Tax Amount",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
    )

    def _create_aml(self):
        self.ensure_one()
        obj_aml = self.env["account.move.line"]
        pair = False
        tax_aml = obj_aml.with_context(check_move_validity=False).create(
            self._prepare_tax_aml_data()
        )
        if self.move_line_id:
            pair = tax_aml + self.move_line_id
        return pair

    @api.model
    def _prepare_aml_data(
        self,
        name,
        account_id,
        debit,
        credit,
        move_id,
    ):
        result = {
            "name": name,
            "account_id": account_id,
            "debit": debit,
            "credit": credit,
            "move_id": move_id,
        }
        return result

    def _get_tax_aml_amount(self):
        self.ensure_one()
        bukpot = self.bukti_potong_id
        debit = credit = 0.0
        if bukpot.direction == "in":
            debit = self.amount_tax
        else:
            credit = self.amount_tax
        return debit, credit

    def _prepare_tax_aml_data(self):
        self.ensure_one()
        bukpot = self.bukti_potong_id
        debit, credit = self._get_tax_aml_amount()
        result = self._prepare_aml_data(
            name=self.name,
            account_id=self._select_tax_account().id,
            debit=debit,
            credit=credit,
            move_id=bukpot.move_id.id,
        )
        return result

    def _select_tax_account(self):
        self.ensure_one()
        tax = self.tax_id
        if tax.invoice_repartition_line_ids:
            result = tax.invoice_repartition_line_ids[1].account_id
        else:
            raise UserWarning(
                _("Please configure invoice tax account for %s") % (tax.name)
            )
        return result
