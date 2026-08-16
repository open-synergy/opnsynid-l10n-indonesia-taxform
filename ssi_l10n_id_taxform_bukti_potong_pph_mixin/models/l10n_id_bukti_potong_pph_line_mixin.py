# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.tools.translate import _


class L10nIdBuktiPotongPphLineMixin(models.AbstractModel):
    """Abstract mixin for a Bukti Potong PPh withholding line.

    Provides the tax line behaviour shared by every concrete Bukti
    Potong PPh document: pairing the withheld ``account.move.line``
    with its source income move line, computing the withheld amount
    and tax, and building the accounting entry lines (``account.move.
    line``) that record the withholding on ``action_done``. Concrete
    transactional models inherit this mixin and add the ``bukti_
    potong_id`` inverse relation via their own ``line_ids`` field.
    """

    _name = "l10n_id.bukti_potong_pph_line_mixin"
    _description = "Bukti Potong PPh Line Mixin"
    _order = "sequence, id"

    @api.depends(
        "income_move_line_ids",
        "income_move_line_ids.debit",
        "income_move_line_ids.credit",
        "amount_computation_method",
        "manual_amount",
    )
    def _compute_amount(self):
        """Compute the withheld amount and the resulting tax amount.

        When ``amount_computation_method`` is ``auto`` the amount is
        summed from ``income_move_line_ids`` (credit side for
        ``direction == "in"``, debit side otherwise). When it is
        ``manual`` the amount is taken from ``manual_amount``. The
        tax amount is then derived by applying ``tax_id`` on the
        resulting amount.
        """
        for line in self:
            line.amount = line.amount_tax = 0.0
            if line.amount_computation_method == "auto":
                for move_line in line.income_move_line_ids:
                    if line.bukti_potong_id.direction == "in":
                        line.amount += move_line.credit
                    else:
                        line.amount += move_line.debit
            else:
                line.amount = line.manual_amount
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
        required=True,
        copy=False,
        ondelete="restrict",
    )

    @api.depends(
        "move_line_id",
    )
    def _compute_allowed_income_move_line_ids(self):
        """Restrict the income move lines selectable for this line.

        Only ``account.move.line`` records that belong to the same
        journal entry as ``move_line_id`` (excluding itself) are
        allowed, so the user can only pick income lines that actually
        originate from the same accounting document.
        """
        AML = self.env["account.move.line"]
        for record in self:
            result = []
            if record.move_line_id:
                criteria = [
                    ("move_id", "=", record.move_line_id.move_id.id),
                    ("id", "!=", record.move_line_id.id),
                ]
                result = AML.search(criteria).ids
            record.allowed_income_move_line_ids = result

    allowed_income_move_line_ids = fields.Many2many(
        string="Allowed Income Move Lines",
        comodel_name="account.move.line",
        compute="_compute_allowed_income_move_line_ids",
    )
    income_move_line_ids = fields.Many2many(
        string="Income Move Lines",
        comodel_name="account.move.line",
    )
    amount = fields.Float(
        string="Amount",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
    )
    amount_computation_method = fields.Selection(
        string="Amount Computation",
        selection=[
            ("auto", "Automatic"),
            ("manual", "Manual"),
        ],
        required=True,
        default="auto",
        readonly=False,
    )
    manual_amount = fields.Float(
        string="Amount (Manual)",
        readonly=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    amount_tax = fields.Float(
        string="Tax Amount",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
    )

    @api.onchange(
        "move_line_id",
        "tax_id",
    )
    def onchange_name(self):
        self.name = False
        if self.move_line_id and self.tax_id:
            name = "%s - %s" % (self.move_line_id.move_id.name, self.tax_id.name)
            self.name = name

    def _create_aml(self):
        """Create the debit/credit tax accounting entry lines.

        Builds one debit and one credit ``account.move.line`` for the
        withheld tax amount and pairs them with ``move_line_id`` so
        they can later be reconciled together.

        :return: the recordset of move lines to reconcile (the source
            ``move_line_id`` plus whichever created line is on the
            opposite side), or ``False`` when the direction is
            unknown
        """
        self.ensure_one()
        AML = self.env["account.move.line"]
        pair = False
        debit_aml = AML.with_context(check_move_validity=False).create(
            self._prepare_tax_debit_aml_data()
        )
        credit_aml = AML.with_context(check_move_validity=False).create(
            self._prepare_tax_credit_aml_data()
        )
        pair = self._pair_aml(debit_aml, credit_aml)
        return pair

    def _pair_aml(self, debit_aml, credit_aml):
        """Select which created line reconciles with ``move_line_id``.

        :param debit_aml: the ``account.move.line`` created on the
            debit side
        :param credit_aml: the ``account.move.line`` created on the
            credit side
        :return: recordset combining ``move_line_id`` with the created
            line on the opposite side of the document direction
        """
        self.ensure_one()
        result = False

        if self.bukti_potong_id.direction == "in":
            result = self.move_line_id + credit_aml
        else:
            result = self.move_line_id + debit_aml

        return result

    def _prepare_aml_data(
        self,
        account_id,
        debit,
        credit,
        partner_id=False,
    ):
        """Build the values for one ``account.move.line``.

        Extension point shared by both the debit and credit tax entry
        preparation methods.

        :param account_id: id of the ``account.account`` to post to
        :param debit: debit amount
        :param credit: credit amount
        :param partner_id: id of the ``res.partner`` on the line, if
            any
        :return: dict of ``account.move.line`` values
        """
        result = {
            "name": self.name,
            "account_id": account_id,
            "debit": debit,
            "credit": credit,
            "move_id": self.bukti_potong_id.move_id.id,
            "partner_id": partner_id,
        }
        return result

    def _get_debit_account(self):
        """Resolve the account for the debit tax entry line.

        For direction ``in`` the tax account (``_select_tax_account``)
        is used; otherwise the account of the source move line is
        used.

        :return: an ``account.account`` record
        """
        self.ensure_one()
        result = False
        if self.bukti_potong_id.direction == "in":
            result = self._select_tax_account()
        else:
            result = self.move_line_id.account_id
        return result

    def _get_credit_account(self):
        """Resolve the account for the credit tax entry line.

        For direction ``out`` the tax account (``_select_tax_account``)
        is used; otherwise the account of the source move line is
        used.

        :return: an ``account.account`` record
        """
        self.ensure_one()
        result = False
        if self.bukti_potong_id.direction == "out":
            result = self._select_tax_account()
        else:
            result = self.move_line_id.account_id
        return result

    def _get_debit_partner(self):
        """Resolve the partner for the debit tax entry line.

        For direction ``in`` the document's ``kpp_id`` (tax office) is
        used; otherwise the partner of the source move line is used.

        :return: a ``res.partner`` record, or ``False``
        """
        self.ensure_one()
        result = False
        if self.bukti_potong_id.direction == "in":
            result = self.bukti_potong_id.kpp_id
        else:
            result = self.move_line_id.partner_id
        return result

    def _get_credit_partner(self):
        """Resolve the partner for the credit tax entry line.

        For direction ``out`` the document's ``kpp_id`` (tax office)
        is used; otherwise the partner of the source move line is
        used.

        :return: a ``res.partner`` record, or ``False``
        """
        self.ensure_one()
        result = False
        if self.bukti_potong_id.direction == "out":
            result = self.bukti_potong_id.kpp_id
        else:
            result = self.move_line_id.partner_id
        return result

    def _prepare_tax_debit_aml_data(self):
        """Build the values for the debit tax entry line.

        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        account = self._get_debit_account()
        partner = self._get_debit_partner()
        return self._prepare_aml_data(
            account_id=account.id,
            debit=self.amount_tax,
            credit=0.0,
            partner_id=partner and partner.id or False,
        )

    def _prepare_tax_credit_aml_data(self):
        """Build the values for the credit tax entry line.

        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        account = self._get_credit_account()
        partner = self._get_credit_partner()
        return self._prepare_aml_data(
            account_id=account.id,
            credit=self.amount_tax,
            debit=0.0,
            partner_id=partner and partner.id or False,
        )

    def _select_tax_account(self):
        """Resolve the tax account configured on ``tax_id``.

        Reads the invoice repartition line's account, which is used
        as the counterpart account for the withheld tax.

        :return: an ``account.account`` record
        :raises UserWarning: when ``tax_id`` has no invoice
            repartition line configured
        """
        self.ensure_one()
        tax = self.tax_id
        if tax.invoice_repartition_line_ids:
            result = tax.invoice_repartition_line_ids[1].account_id
        else:
            raise UserWarning(
                _("Please configure invoice tax account for %s") % (tax.name)
            )
        return result
