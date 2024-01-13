# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class FakturPajakKeluaran(models.Model):
    _name = "faktur_pajak_keluaran"
    _inherit = [
        "mixin.transaction_terminate",
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.transaction_partner",
        "mixin.transaction_untaxed_with_field",
        "mixin.transaction_total_with_field",
        "mixin.transaction_tax_with_field",
        "mixin.company_currency",
        "mixin.account_move",
        "mixin.many2one_configurator",
    ]
    _description = "Faktur Pajak Keluaran"

    # mixin.multiple_approval attributes
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_open_button = False
    _automatically_insert_open_policy_fields = False

    # Attributes related to add element on form view automatically
    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "terminate_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve",
        "action_reject",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "%(ssi_transaction_cancel_mixin.base_select_terminate_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_open",
        "dom_done",
        "dom_cancel",
        "dom_terminate",
        "dom_reject",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    # mixin.transaction_untaxed attributes
    _detail_object_name = "detail_ids"
    _detail_amount_field_name = "price_subtotal"
    _amount_untaxed_field_name = "amount_untaxed"

    # mixin.transaction_tax attributes
    _tax_detail_object_name = "tax_ids"
    _tax_detail_amount_field_name = "tax_amount"
    _amount_tax_field_name = "amount_tax"

    # mixin.transaction_total attributes
    _amount_untaxed_field_name = "amount_untaxed"
    _amount_tax_field_name = "amount_tax"
    _amount_total_field_name = "amount_total"

    # mixin.transaction_tax attributes
    _tax_lines_field_name = "tax_ids"
    _tax_on_self = False
    _tax_source_recordset_field_name = "detail_ids"
    _price_unit_field_name = "price_unit"
    _quantity_field_name = "uom_quantity"

    date = fields.Date(
        string="Date",
        copy=False,
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    currency_id = fields.Many2one(
        related="company_currency_id",
    )
    taxform_period_id = fields.Many2one(
        string="Masa Pajak",
        comodel_name="l10n_id.tax_period",
        compute="_compute_taxform_period",
        store=True,
        copy=False,
    )
    taxform_year_id = fields.Many2one(
        string="Tahun Pajak",
        comodel_name="l10n_id.tax_year",
        compute="_compute_taxform_year",
        store=True,
        copy=False,
    )
    allowed_fpk_journal_ids = fields.Many2many(
        string="Allowed FP Keluaran Journal",
        comodel_name="account.journal",
        compute="_compute_allowed_fpk_journal_ids",
        compute_sudo=True,
        store=False,
    )
    allowed_fpk_account_ids = fields.Many2many(
        string="Allowed FP Keluaran Accounts",
        comodel_name="account.account",
        compute="_compute_allowed_fpk_account_ids",
        compute_sudo=True,
        store=False,
    )
    allowed_fpk_tax_ids = fields.Many2many(
        string="Allowed FP Keluaran Taxes",
        comodel_name="account.tax",
        compute="_compute_allowed_fpk_tax_ids",
        compute_sudo=True,
        store=False,
    )

    type_id = fields.Many2one(
        string="Transaction Type",
        comodel_name="faktur_pajak_transaction_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    enofa_number_id = fields.Many2one(
        string="# E-NOFA",
        comodel_name="enofa_number",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    tax_id = fields.Many2one(
        string="Tax",
        comodel_name="account.tax",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_enofa_number_ids = fields.Many2many(
        string="Allowed E-NOFA Numbers",
        comodel_name="enofa_number",
        compute="_compute_allowed_enofa_number_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_move_ids = fields.Many2many(
        string="Allowed Journal Entries",
        comodel_name="account.move",
        compute="_compute_allowed_move_ids",
        store=False,
        compute_sudo=True,
    )
    move_ids = fields.Many2many(
        string="Journal Entries",
        comodel_name="account.move",
        relation="el_faktur_pajak_keluaran_2_journal_entry",
        column1="faktur_pajak_keluaran_id",
        column2="move_id",
    )
    allowed_move_line_ids = fields.Many2many(
        string="Allowed Journal Items",
        comodel_name="account.move.line",
        compute="_compute_allowed_move_line_ids",
        store=False,
        compute_sudo=True,
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="faktur_pajak_keluaran_detail",
        inverse_name="faktur_pajak_keluaran_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    tax_ids = fields.One2many(
        string="Taxes",
        comodel_name="faktur_pajak_keluaran_tax",
        inverse_name="faktur_pajak_keluaran_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.depends("type_id")
    def _compute_allowed_fpk_journal_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="account.journal",
                    method_selection=record.type_id.fpk_journal_selection_method,
                    manual_recordset=record.type_id.fpk_journal_ids,
                    domain=record.type_id.fpk_journal_domain,
                    python_code=record.type_id.fpk_journal_python_code,
                )
            record.allowed_fpk_journal_ids = result

    @api.depends("type_id")
    def _compute_allowed_fpk_account_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="account.account",
                    method_selection=record.type_id.fpk_account_selection_method,
                    manual_recordset=record.type_id.fpk_account_ids,
                    domain=record.type_id.fpk_account_domain,
                    python_code=record.type_id.fpk_account_python_code,
                )
            record.allowed_fpk_account_ids = result

    @api.depends("type_id")
    def _compute_allowed_fpk_tax_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="account.tax",
                    method_selection=record.type_id.fpk_tax_selection_method,
                    manual_recordset=record.type_id.fpk_tax_ids,
                    domain=record.type_id.fpk_tax_domain,
                    python_code=record.type_id.fpk_tax_python_code,
                )
            record.allowed_fpk_tax_ids = result

    @api.depends(
        "type_id",
        "partner_id",
    )
    def _compute_allowed_move_ids(self):
        AM = self.env["account.move"]
        for record in self:
            result = False
            if record.type_id and record.partner_id:
                criteria1 = [
                    ("faktur_pajak_keluaran_id", "=", False),
                    ("state", "=", "posted"),
                    ("journal_id", "in", record.allowed_fpk_journal_ids.ids),
                    ("partner_id.commercial_partner_id.id", "=", record.partner_id.id),
                ]
                result = AM.search(criteria1)
                criteria2 = [
                    ("faktur_pajak_keluaran_id", "!=", False),
                    ("fp_keluaran_state", "in", ["cancelled"]),
                    ("state", "=", "posted"),
                    ("journal_id", "in", record.allowed_fpk_journal_ids.ids),
                    ("partner_id.commercial_partner_id.id", "=", record.partner_id.id),
                ]
                result += AM.search(criteria2)
            record.allowed_move_ids = result

    @api.depends(
        "company_id",
        "taxform_year_id",
    )
    def _compute_allowed_enofa_number_ids(self):
        for record in self:
            result = False
            ENofaNumber = self.env["enofa_number"]
            if record.company_id and record.taxform_year_id:
                criteria = [
                    ("enofa_id.company_id", "=", self.company_id.id),
                    ("enofa_id.tax_year_id", "=", self.taxform_year_id.id),
                    ("state", "=", "unused"),
                ]
                result = ENofaNumber.search(criteria).ids
            record.allowed_enofa_number_ids = result

    @api.depends(
        "move_ids",
    )
    def _compute_allowed_move_line_ids(self):
        for record in self:
            result = False
            AML = self.env["account.move.line"]
            if record.move_ids:
                criteria = [
                    ("move_id", "in", record.move_ids.ids),
                    ("credit", ">", 0.0),
                    ("tax_ids", "!=", False),
                    ("account_id", "in", record.allowed_fpk_account_ids.ids),
                    ("tax_ids", "in", self.allowed_fpk_tax_ids.ids),
                ]
                result = AML.search(criteria).ids
            record.allowed_move_line_ids = result

    @api.depends(
        "date",
    )
    def _compute_taxform_period(self):
        for fp in self:
            fp.taxform_period_id = False
            if fp.date:
                fp.taxform_period_id = (
                    self.env["l10n_id.tax_period"]._find_period(fp.date).id
                )

    @api.depends(
        "taxform_period_id",
    )
    def _compute_taxform_year(self):
        for fp in self:
            fp.taxform_year_id = False
            if fp.taxform_period_id:
                fp.taxform_year_id = fp.taxform_period_id.year_id.id

    @api.onchange(
        "type_id",
    )
    def onchange_tax_id(self):
        self.tax_id = False
        if self.type_id:
            self.tax_id = self.type_id.tax_id

    def action_reload_detail(self):
        Detail = self.env["faktur_pajak_keluaran_detail"]
        self.detail_ids.unlink()
        for record in self.sudo():
            if record.allowed_move_line_ids:
                for aml in record.allowed_move_line_ids:
                    data = {
                        "faktur_pajak_keluaran_id": self.id,
                        "name": (aml.product_id and aml.product_id.name)
                        or aml.name
                        or "-",
                        "account_id": aml.account_id.id,
                        "product_id": aml.product_id and aml.product_id.id,
                        "uom_quantity": aml.quantity or 1.0,
                        "uom_id": aml.product_uom_id and aml.product_uom_id.id,
                        "price_unit": aml.credit,
                        "tax_ids": [(6, 0, [self.tax_id.id])],
                    }
                    Detail.create(data)
        self._recompute_standard_tax()

    @api.model
    def _get_policy_field(self):
        res = super(FakturPajakKeluaran, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "done_ok",
            "cancel_ok",
            "terminate_ok",
            "restart_ok",
            "reject_ok",
            "manual_number_ok",
            "restart_approval_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
