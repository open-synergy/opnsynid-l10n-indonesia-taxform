# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import Warning as UserError
from odoo.tools.translate import _


class L10nIdBuktiPotongPphMixin(models.AbstractModel):
    """Abstract mixin for an Indonesian Bukti Potong PPh document.

    Provides the transactional workflow (draft/confirm/done/cancel via
    ``mixin.transaction_confirm``/``done``/``cancel``) shared by every
    concrete Bukti Potong PPh withholding-tax slip: computing the
    total withheld tax from ``line_ids``, creating the accounting
    journal entry and its tax lines on ``action_done``, and reversing
    that entry on ``action_cancel``. Concrete transactional models
    inherit this mixin and set ``type_id`` (via ``_default_type_id``)
    to the specific Bukti Potong PPh form they represent.
    """

    _name = "l10n_id.bukti_potong_pph_mixin"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
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
        """Return the id of the current user's company.

        Used as the default value for the ``company_id`` field
        provided by the transaction mixins.

        :return: id of a ``res.company`` record
        """
        return self.env.user.company_id.id

    def _default_type_id(self):
        """Return the default ``type_id`` for this document.

        Base implementation returns ``False``; concrete models
        override this to always default to their specific Bukti
        Potong PPh form type.

        :return: id of a ``l10n_id.bukti_potong_pph_type`` record, or
            ``False``
        """
        return False

    @api.model
    def _default_wajib_pajak_id(self):
        """Default the taxpayer (Wajib Pajak) for direction ``in``.

        When the document type's direction is ``in`` the current
        company's partner is the one being withheld from, so it is
        defaulted as ``wajib_pajak_id``.

        :return: id of a ``res.partner`` record, or ``False``
        """
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
        """Default the withholding party (Pemotong Pajak) for ``out``.

        When the document type's direction is ``out`` the current
        company's partner is the one doing the withholding, so it is
        defaulted as ``pemotong_pajak_id``.

        :return: id of a ``res.partner`` record, or ``False``
        """
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
        """Return today's date as the default document date.

        :return: today's date, formatted ``%Y-%m-%d``
        """
        return datetime.now().strftime("%Y-%m-%d")

    @api.depends(
        "line_ids",
        "line_ids.amount_tax",
    )
    def _compute_tax(self):
        """Sum the withheld tax amount from all lines.

        Stores the automatic total in ``total_tax``, used as the
        input for ``_compute_total_tax``.
        """
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
        """Compute the final total tax and the manual/auto difference.

        ``total_tax_diff`` is always the difference between the
        manually entered total and the automatic total, so it can be
        posted as a correction entry. ``total_tax_final`` follows
        ``total_tax`` when ``total_tax_computation`` is ``auto``, or
        ``manual_total_tax`` when it is ``manual``.
        """
        for record in self:
            record.total_tax_diff = record.manual_total_tax - record.total_tax
            if record.total_tax_computation == "auto":
                record.total_tax_final = record.total_tax
            else:
                record.total_tax_final = record.manual_total_tax

    type_id = fields.Many2one(
        string="Form Type",
        comodel_name="l10n_id.bukti_potong_pph_type",
        ondelete="restrict",
        required=True,
        readonly=True,
    )
    direction = fields.Selection(
        string="Type",
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

    tax_period_id = fields.Many2one(
        string="Tax Period",
        comodel_name="l10n_id.tax_period",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
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
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    manual_total_tax = fields.Float(
        string="Total Tax (Manual)",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
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
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    diff_credit_account_id = fields.Many2one(
        string="Diff. Credit Account",
        comodel_name="account.account",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
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

    @api.depends(
        "type_id",
        "wajib_pajak_id",
        "pemotong_pajak_id",
    )
    def _compute_allowed_move_line(self):
        """Restrict the accounting move lines selectable for lines.

        Only ``account.move.line`` records that are unreconciled and
        match ``_prepare_domain_allowed_move_lines`` are allowed, and
        only once ``type_id``, ``wajib_pajak_id``, and
        ``pemotong_pajak_id`` are all set.
        """
        AML = self.env["account.move.line"]
        for record in self:
            result = []
            if record.type_id and record.wajib_pajak_id and record.pemotong_pajak_id:
                criteria = record._prepare_domain_allowed_move_lines()
                result = AML.search(criteria).ids
            record.allowed_move_line_ids = result

    def _prepare_domain_allowed_move_lines(self):
        """Build the search domain for ``_compute_allowed_move_line``.

        Restricts to unreconciled lines on ``account_id``, further
        filtered by the counterpart partner: ``pemotong_pajak_id`` for
        direction ``in``, ``wajib_pajak_id`` otherwise.

        :return: a search domain (list of tuples)
        """
        self.ensure_one()
        result = [
            ("account_id", "=", self.account_id.id),
            ("reconciled", "=", False),
        ]
        if self.direction == "in":
            result.append(("partner_id", "=", self.pemotong_pajak_id.id))
        else:
            result.append(("partner_id", "=", self.wajib_pajak_id.id))
        return result

    allowed_move_line_ids = fields.Many2many(
        string="Allowed Move Lines",
        comodel_name="account.move.line",
        compute="_compute_allowed_move_line",
    )
    move_id = fields.Many2one(
        string="Accounting Entry",
        comodel_name="account.move",
        readonly=True,
        copy=False,
    )

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
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
        "date",
    )
    def onchange_tax_period(self):
        """Default ``tax_period_id`` from ``date``.

        Looks up the tax period covering ``date``; falls back to
        clearing ``tax_period_id`` when no matching period is found.
        """
        obj_tax_period = self.env["l10n_id.tax_period"]
        try:
            self.tax_period_id = obj_tax_period._find_period(self.date)
        except Exception:
            self.tax_period_id = False

    @api.onchange(
        "type_id",
    )
    def onchange_policy_template_id(self):
        """Default ``policy_template_id`` based on the document type.

        Delegates to ``_get_template_policy`` (provided by
        ``mixin.policy``) so the approval policy template follows
        whichever ``type_id`` is selected.
        """
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

    @api.constrains(
        "total_tax_final",
    )
    def _constrains_total_tax_final(self):
        """Require a positive total tax when the document has lines.

        :raises UserError: when ``total_tax_final`` is not greater
            than zero while ``line_ids`` is not empty
        """
        for record in self:
            if record.total_tax_final <= 0.0 and len(record.line_ids) > 0:
                raise UserError(_("Total tax has to be greater than 0"))

    def action_done(self):
        """Complete the document and create its accounting entries.

        Runs the base ``action_done`` transition, then creates the
        tax accounting entry lines (``_create_aml``) for every line
        of the document.
        """
        _super = super()
        _super.action_done()
        for bukpot in self.sudo():
            bukpot._create_aml()

    def _prepare_done_data(self):
        """Extend the ``done`` write values with the journal entry.

        Creates the journal entry (``_create_journal_entry``) and
        adds its id as ``move_id`` to the values prepared by the base
        mixin.

        :return: dict of values to write when transitioning to
            ``done``
        """
        self.ensure_one()
        _super = super()
        result = _super._prepare_done_data()
        move = self._create_journal_entry()
        result.update(
            {
                "move_id": move.id,
            }
        )
        return result

    def _create_journal_entry(self):
        """Create the ``account.move`` journal entry for this document.

        :return: the created ``account.move`` record
        """
        self.ensure_one()
        Move = self.env["account.move"]
        move = Move.create(self._prepare_journal_entry_data())
        return move

    def _prepare_journal_entry_data(self):
        """Build the values for the document's journal entry.

        :return: dict of ``account.move`` values
        """
        self.ensure_one()
        data = {
            "name": self.name,
            "date": self.date,
            "journal_id": self.journal_id.id,
        }
        return data

    def _create_aml(self):
        """Create, post, and reconcile the document's tax entry lines.

        Delegates to every line's ``_create_aml`` to build the tax
        entry lines, posts the journal entry, reconciles each
        resulting pair, and finally creates the manual/auto
        difference entry (``_create_aml_diff``) when applicable.
        """
        self.ensure_one()
        pairs = []
        for line in self.line_ids:
            pairs.append(line._create_aml())

        self.move_id.action_post()

        for pair in pairs:
            pair.reconcile()

        if self.total_tax_computation == "manual" and self.total_tax_diff != 0.0:
            self._create_aml_diff()

    def action_cancel(self, cancel_reason=False):
        """Cancel the document and undo its accounting entries.

        Runs the base ``action_cancel`` transition, then removes the
        reconciliation and deletes the journal entry that was created
        on ``action_done``.

        :param cancel_reason: optional ``base.cancel.reason`` record
            explaining the cancellation
        :return: result of the base ``action_cancel``
        """
        _super = super()
        res = _super.action_cancel(cancel_reason)
        for bukpot in self.sudo():
            bukpot.move_id.line_ids.remove_move_reconcile()
            bukpot.move_id.with_context(force_delete=True).unlink()
        return res

    def _create_aml_diff(self):
        """Create the correction entry for the manual/auto tax diff.

        Posts one credit and one debit line for ``total_tax_diff`` on
        the configured diff accounts.
        """
        self.ensure_one()
        AML = self.env["account.move.line"]
        AML.with_context(check_move_validity=False).create(
            self._prepare_credit_aml_diff()
        )
        AML.with_context(check_move_validity=False).create(
            self._prepare_debit_aml_diff()
        )

    def _prepare_aml_diff(self, account):
        """Build the values for one diff correction move line.

        :param account: the ``account.account`` to post the diff to
        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        name = "Taxform diff %s" % (self.name)
        amount = abs(self.total_tax_diff)
        return {
            "name": name,
            "account_id": account.id,
            "debit": amount,
            "credit": amount,
            "move_id": self.move_id.id,
        }

    def _prepare_debit_aml_diff(self):
        """Build the values for the debit diff correction move line.

        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        account = self._get_diff_debit_account()
        result = self._prepare_aml_diff(account)
        return result

    def _prepare_credit_aml_diff(self):
        """Build the values for the credit diff correction move line.

        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        account = self._get_diff_credit_account()
        result = self._prepare_aml_diff(account)
        return result

    def _get_diff_debit_account(self):
        """Return the configured debit diff account.

        :return: the ``diff_debit_account_id`` record
        :raises UserError: when ``diff_debit_account_id`` is not set
        """
        self.ensure_one()
        if not self.diff_debit_account_id:
            error_msg = _("Debit diff. account not defined")
            raise UserError(error_msg)
        return self.diff_debit_account_id

    def _get_diff_credit_account(self):
        """Return the configured credit diff account.

        :return: the ``diff_credit_account_id`` record
        :raises UserError: when ``diff_credit_account_id`` is not set
        """
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
        """Default ``wajib_pajak_id`` when ``type_id``/``company_id``
        change.

        Note the field written is ``wajib_pajak_id``, mirroring
        ``_default_pemotong_pajak_id``'s direction logic; kept as-is
        since this is existing behaviour, not part of this change.
        """
        self.wajib_pajak_id = self._default_pemotong_pajak_id()

    @api.onchange("type_id", "company_id")
    def onchange_wajib_pajak_id(self):
        """Default ``wajib_pajak_id`` when ``type_id``/``company_id``
        change.
        """
        self.wajib_pajak_id = self._default_wajib_pajak_id()
