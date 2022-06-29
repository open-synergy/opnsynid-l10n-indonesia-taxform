# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import Warning as UserError
from odoo.tools.translate import _


class BuktiPotongPPhMixin(models.AbstractModel):
    _name = "l10n_id.bukti_potong_pph_mixin"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
    ]
    _description = "Bukti Potong PPh"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_button = False
    _automatically_insert_done_policy_fields = False

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    def _default_company_id(self):
        return self.env.user.company_id.id

    def _default_type_id(self):
        return False

    @api.model
    def _default_wajib_pajak_id(self):
        obj_type = self.env["l10n_id.bukti_potong_pph_type"]
        type_id = self._default_type_id()
        if not type_id:
            return False
        direction = obj_type.browse(type_id)[0].direction
        if direction == "in":
            return self.env.user.company_id.partner_id.id
        else:
            return False

    @api.model
    def _default_pemotong_pajak_id(self):
        obj_type = self.env["l10n_id.bukti_potong_pph_type"]
        type_id = self._default_type_id()
        if not type_id:
            return False
        direction = obj_type.browse(type_id)[0].direction
        if direction == "out":
            return self.env.user.company_id.partner_id.id
        else:
            return False

    @api.model
    def _default_date(self):
        return datetime.now().strftime("%Y-%m-%d")

    @api.depends(
        "line_ids",
        "line_ids.amount_tax",
    )
    def _compute_tax(self):
        for bukpot in self:
            bukpot.total_tax = 0.0
            for line in bukpot.line_ids:
                bukpot.total_tax += line.amount_tax

    @api.depends(
        "total_tax",
        "total_tax_computation",
        "manual_total_tax",
    )
    def _compute_total_tax(self):
        for record in self:
            record.total_tax_diff = record.manual_total_tax - record.total_tax
            if record.total_tax_computation == "auto":
                record.total_tax_final = record.total_tax
            else:
                record.total_tax_final = record.manual_total_tax

    name = fields.Char(
        string="# Bukti Potong",
        required=True,
        default="/",
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    type_id = fields.Many2one(
        string="Form Type",
        comodel_name="l10n_id.bukti_potong_pph_type",
        ondelete="restrict",
        required=True,
        readonly=True,
    )
    direction = fields.Selection(
        string="Type",
        selection=[
            ("in", "In"),
            ("out", "Out"),
        ],
        related="type_id.direction",
        store=True,
        readonly=True,
    )
    allowed_journal_ids = fields.Many2many(
        string="Allowed Journals",
        comodel_name="account.journal",
        related="type_id.journal_ids",
        # compute="_compute_allowed_journal",
        store=False,
        compute_sudo=True,
    )
    allowed_tax_ids = fields.Many2many(
        string="Allowed Tax",
        comodel_name="account.tax",
        related="type_id.tax_ids",
        # compute="_compute_allowed_tax",
        store=False,
        compute_sudo=True,
    )
    allowed_account_ids = fields.Many2many(
        string="Allowed Accounts",
        comodel_name="account.account",
        related="type_id.account_ids",
        # compute="_compute_allowed_account",
        store=False,
        compute_sudo=True,
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=lambda self: self._default_date(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "date",
    )
    def _compute_tax_period(self):
        obj_tax_period = self.env["l10n_id.tax_period"]
        for bukpot in self:
            try:
                bukpot.tax_period_id = obj_tax_period._find_period(bukpot.date)
            except Exception:
                bukpot.tax_period_id = False

    tax_period_id = fields.Many2one(
        string="Tax Period",
        comodel_name="l10n_id.tax_period",
        compute="_compute_tax_period",
        store=True,
        compute_sudo=True,
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    kpp_id = fields.Many2one(
        string="KPP",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    wajib_pajak_id = fields.Many2one(
        string="Wajib Pajak",
        comodel_name="res.partner",
        required=True,
        ondelete="restrict",
        default=lambda self: self._default_wajib_pajak_id(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    pemotong_pajak_id = fields.Many2one(
        string="Pemotong Pajak",
        comodel_name="res.partner",
        required=True,
        ondelete="restrict",
        default=lambda self: self._default_pemotong_pajak_id(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    ttd_id = fields.Many2one(
        string="TTD",
        comodel_name="res.partner",
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    total_tax = fields.Float(
        string="Total Tax (Auto)",
        compute="_compute_tax",
        store=True,
        compute_sudo=True,
    )
    total_tax_computation = fields.Selection(
        string="Total Tax Computation",
        selection=[
            ("auto", "Automatic"),
            ("manual", "Manual"),
        ],
        required=True,
        default="auto",
    )
    manual_total_tax = fields.Float(
        string="Total Tax (Manual)",
    )
    total_tax_diff = fields.Float(
        string="Total Tax Diff.",
        compute="_compute_total_tax",
        store=True,
        compute_sudo=True,
    )
    diff_debit_account_id = fields.Many2one(
        string="Diff. Debit Account",
        comodel_name="account.account",
    )
    diff_credit_account_id = fields.Many2one(
        string="Diff. Credit Account",
        comodel_name="account.account",
    )
    total_tax_final = fields.Float(
        string="Total Tax",
        compute="_compute_total_tax",
        store=True,
        compute_sudo=True,
    )

    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        default="draft",
        copy=False,
    )
    line_ids = fields.One2many(
        string="Bukti Potong Line",
        comodel_name="l10n_id.bukti_potong_pph_line_mixin",
        inverse_name="bukti_potong_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    move_id = fields.Many2one(
        string="Accounting Entry",
        comodel_name="account.move",
        readonly=True,
        copy=False,
    )

    @api.model
    def _get_policy_field(self):
        res = super(BuktiPotongPPhMixin, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.onchange(
        "type_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

    def action_done(self):
        _super = super(BuktiPotongPPhMixin, self)
        _super.action_done()
        # Saat Done lakukan proses penjurnalan di account move dan aml
        # run prepare_action_done on action_done
        for bukpot in self.sudo():
            # create journal item (aml)
            bukpot._create_aml()

    def _prepare_done_data(self):
        self.ensure_one()
        _super = super(BuktiPotongPPhMixin, self)
        result = _super._prepare_done_data()
        # Process create journal entry di account move
        move = self._create_journal_entry()
        result.update(
            {
                "move_id": move.id,
            }
        )
        return result

    def _create_journal_entry(self):
        self.ensure_one()
        obj_move = self.env["account.move"]
        if self.total_tax_final <= 0.0:
            raise UserError(_("Total tax has to be greater than 0"))
        # Prosess prepapre data
        move = obj_move.create(self._prepare_journal_entry_data())
        return move

    def _prepare_journal_entry_data(self):
        self.ensure_one()
        data = {
            "name": self.name,
            "date": self.date,
            "journal_id": self.journal_id.id,
        }
        return data

    def _create_aml(self):
        self.ensure_one()
        obj_move_line = self.env["account.move.line"]
        # Prosess prepare data aml header
        obj_move_line.with_context(check_move_validity=False).create(
            self._prepare_data_aml()
        )
        for line in self.line_ids:
            # process line on account move
            line._create_aml()
        if self.total_tax_diff != 0.0:
            self._create_aml_diff()

    def _prepare_data_aml(self):
        self.ensure_one()
        debit, credit = self._get_aml_amount()
        result = {
            "name": self.name,
            "account_id": self.account_id.id,
            "debit": debit,
            "credit": credit,
            "move_id": self.move_id.id,
        }
        return result

    def _get_aml_amount(self):
        self.ensure_one()
        debit = credit = 0.0
        if self.direction == "out":
            debit = self.total_tax_final
        else:
            credit = self.total_tax_final
        return debit, credit

    def action_cancel(self, cancel_reason=False):
        _super = super(BuktiPotongPPhMixin, self)
        res = _super.action_cancel(cancel_reason)
        for bukpot in self.sudo():
            if bukpot._check_move():
                bukpot.move_id.button_cancel()
            bukpot.move_id.unlink()
        return res

    def _check_move(self):
        self.ensure_one()
        result = False
        if self.move_id.state == "posted":
            result = True
        return result

    def _create_aml_diff(self):
        self.ensure_one()
        if self.direction == "in":
            self.env["account.move.line"].with_context(
                check_move_validity=False
            ).create(self._prepare_credit_aml_diff())
        else:
            self.env["account.move.line"].with_context(
                check_move_validity=False
            ).create(self._prepare_debit_aml_diff())

    def _prepare_debit_aml_diff(self):
        self.ensure_one()
        debit = abs(self.total_tax_diff)
        credit = 0.0
        name = "Taxform diff %s" % (self.name)
        result = {
            "name": name,
            "account_id": self._get_diff_debit_account().id,
            "debit": debit,
            "credit": credit,
            "move_id": self.move_id.id,
        }
        return result

    def _prepare_credit_aml_diff(self):
        self.ensure_one()
        debit = 0.0
        credit = abs(self.total_tax_diff)
        name = "Taxform diff %s" % (self.name)
        result = {
            "name": name,
            "account_id": self._get_diff_credit_account().id,
            "credit": credit,
            "debit": debit,
            "move_id": self.move_id.id,
        }
        return result

    def _get_diff_debit_account(self):
        self.ensure_one()
        if not self.diff_debit_account_id:
            error_msg = _("Debit diff. account not defined")
            raise UserError(error_msg)
        return self.diff_debit_account_id

    def _get_diff_credit_account(self):
        self.ensure_one()
        if not self.diff_credit_account_id:
            error_msg = _("Credit diff. account not defined")
            raise UserError(error_msg)
        return self.diff_credit_account_id

    @api.onchange("pemotong_pajak_id")
    def onchange_ttd_id(self):
        self.ttd_id = False

    @api.onchange("type_id", "company_id")
    def onchange_pemotong_pajak_id(self):
        self.wajib_pajak_id = self._default_pemotong_pajak_id()

    @api.onchange("type_id", "company_id")
    def onchange_wajib_pajak_id(self):
        self.wajib_pajak_id = self._default_wajib_pajak_id()

    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for bukti_potong in self:
            if bukti_potong.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(BuktiPotongPPhMixin, self)
        _super.unlink()

    def name_get(self):
        result = []
        for record in self:
            if record.name == "/":
                name = "*" + str(record.id)
            else:
                name = record.name
            result.append((record.id, name))
        return result
