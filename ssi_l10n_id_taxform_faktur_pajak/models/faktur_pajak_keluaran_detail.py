# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class FakturPajakKeluaranDetail(models.Model):
    _name = "faktur_pajak_keluaran_detail"
    _description = "Detail Faktur Pajak Keluaran"
    _inherit = ["mixin.product_line_account"]

    faktur_pajak_keluaran_id = fields.Many2one(
        comodel_name="faktur_pajak_keluaran",
        string="# Faktur Pajak Keluaran",
        required=True,
        ondelete="cascade",
    )
    base_amount = fields.Monetary(
        string="Base Amount (DPP)",
        currency_field="currency_id",
        help="Tax-exclusive unit base copied from the source invoice "
        "line's accounting entry (never affected by which tax is "
        "selected on this line). Used to re-derive `price_unit` "
        "whenever `tax_ids` changes, so the DPP stays correct whether "
        "the selected tax is Include or Exclude. Left empty for lines "
        "not sourced from an invoice (e.g. added manually), which keep "
        "the legacy behaviour of `price_unit` being edited directly.",
    )

    @api.onchange(
        "tax_ids",
    )
    def onchange_price_unit_from_base_amount(self):
        """Re-derive `price_unit` as soon as the line's tax is changed.

        Delegates to `_recompute_price_unit_from_base_amount` so the UI
        reflects the corrected DPP/PPN immediately when a user swaps a
        detail line's tax in the tree view, without waiting for the
        "Compute Tax" button.
        """
        self._recompute_price_unit_from_base_amount()

    def _recompute_price_unit_from_base_amount(self):
        """Re-derive `price_unit` from `base_amount` for the current tax.

        `price_unit` is fed into the standard `account.tax.compute_all`
        (via `mixin.product_line_account`), which treats it as
        tax-inclusive when the tax is a price-included ("Include") tax
        and as tax-exclusive otherwise. `base_amount` is always the
        tax-exclusive DPP, so when an Include tax is selected,
        `price_unit` must be grossed up first -- otherwise the tax gets
        stripped a second time and the DPP/PPN reported to Coretax end
        up smaller than the source invoice. Delegates the actual
        gross-up to `_gross_up_price_unit_for_tax`, which works for any
        Include tax formula (plain `percent` or a custom
        `python_compute` "code" tax).
        """
        for record in self:
            if not record.base_amount:
                continue
            tax = record.tax_ids[:1]
            record.price_unit = record._gross_up_price_unit_for_tax(
                record.base_amount, tax
            )

    def _gross_up_price_unit_for_tax(self, base_amount, tax):
        """Find the `price_unit` whose exclusive total equals `base_amount`.

        For no tax, or an Exclude tax, `price_unit` already equals the
        exclusive base, so `base_amount` is returned unchanged.

        For an Include tax, `compute_all` treats `price_unit` as
        already tax-inclusive and strips the tax back out of it; that
        is inverted here by adjusting `price_unit` until
        `compute_all`'s own `total_excluded` matches `base_amount`,
        instead of assuming a particular tax formula. VAT-style taxes
        are proportional to `price_unit` (no fixed component), so
        `total_excluded / price_unit` is their exact slope and a
        single correction scaled by that ratio converges in one or two
        iterations -- whether the tax is a plain `percent` type or a
        custom `python_compute` "code" tax, such as the one "PPN
        Keluaran 11% (Include)" was reconfigured to on the SGRS
        production server (``gross * 11 / 111``, mathematically
        equivalent to a plain 11% Include tax but not something that
        can be read off `tax.amount`/`tax.amount_type` directly).
        Capped defensively so a pathological tax formula cannot loop
        forever; it then returns its best-effort result rather than
        raising.
        """
        self.ensure_one()
        if not tax or not tax.price_include:
            return base_amount
        quantity = self.uom_quantity or 1.0
        currency = self.currency_id or self.env.company.currency_id
        precision = currency.rounding or 0.01
        target_total = base_amount * quantity
        price_unit = base_amount
        for _iteration in range(20):
            total_excluded = tax.compute_all(
                price_unit,
                currency,
                quantity,
                product=self.product_id,
                partner=False,
            )["total_excluded"]
            diff = target_total - total_excluded
            if abs(diff) < precision:
                break
            ratio = total_excluded / price_unit if price_unit else 0.0
            if ratio <= 0:
                price_unit += diff / quantity
            else:
                price_unit += (diff / quantity) / ratio
        return price_unit

    @api.constrains(
        "tax_ids",
        "faktur_pajak_keluaran_id",
    )
    def _check_tax_allowed_by_type(self):
        """Ensure the line's tax is allowed by the parent's type.

        Validates that every tax on ``tax_ids`` belongs to
        ``faktur_pajak_keluaran_id.allowed_fpk_tax_ids`` -- the
        whitelist computed from the parent's transaction type. When
        the whitelist is unrestricted (empty/``False``, e.g. the
        default domain ``"[]"`` matches every ``account.tax``), the
        check is skipped instead of blocking everything. Declared on
        this model (not on the parent) because Odoo's
        ``@api.constrains`` does not re-trigger a parent's constraint
        when a one2many child field changes.

        :raises ValidationError: when a tax on ``tax_ids`` is not part
            of the parent's ``allowed_fpk_tax_ids``.
        """
        for record in self:
            fpk = record.faktur_pajak_keluaran_id
            if not fpk.type_id or not fpk.allowed_fpk_tax_ids:
                continue

            invalid_taxes = record.tax_ids - fpk.allowed_fpk_tax_ids
            if invalid_taxes:
                error_message = """
                Context: Set detail line tax
                Database ID: %s
                Problem: Tax %s on line %s is not allowed for \
transaction type %s
                Solution: Pick a tax allowed by the transaction type
                """ % (
                    fpk.id,
                    ", ".join(invalid_taxes.mapped("name")),
                    record.name,
                    fpk.type_id.name,
                )
                raise ValidationError(_(error_message))

    @api.depends(
        "name",
    )
    def _compute_efaktur_of_name(self):
        for record in self:
            result = False
            if record.name:
                result = record.name
            record.efaktur_of_name = result

    efaktur_of_name = fields.Char(
        string="OF_NAMA",
        compute="_compute_efaktur_of_name",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "product_id",
        "product_id.code",
    )
    def _compute_efaktur_of_code(self):
        for record in self:
            result = False
            if record.product_id and record.product_id.code:
                result = record.product_id.code
            record.efaktur_of_code = result

    efaktur_of_code = fields.Char(
        string="OF_KODE",
        compute="_compute_efaktur_of_code",
        store=True,
        compute_sudo=True,
    )

    @api.depends("price_unit")
    def _compute_efaktur_of_harga_satuan(self):
        for record in self:
            record.efaktur_of_harga_satuan = str(record.price_unit)

    efaktur_of_harga_satuan = fields.Char(
        string="OF_HARGA_SATUAN",
        compute="_compute_efaktur_of_harga_satuan",
        store=True,
        compute_sudo=True,
    )

    @api.depends("uom_quantity")
    def _compute_efaktur_of_jumlah_barang(self):
        for record in self:
            record.efaktur_of_jumlah_barang = str(record.uom_quantity)

    efaktur_of_jumlah_barang = fields.Char(
        string="OF_JUMLAH_BARANG",
        compute="_compute_efaktur_of_jumlah_barang",
        store=True,
        compute_sudo=True,
    )

    @api.depends("price_subtotal")
    def _compute_efaktur_of_harga_total(self):
        for record in self:
            record.efaktur_of_harga_total = str(record.price_subtotal)

    efaktur_of_harga_total = fields.Char(
        string="OF_HARGA_TOTAL",
        compute="_compute_efaktur_of_harga_total",
        store=True,
        compute_sudo=True,
    )

    @api.depends("price_subtotal")
    def _compute_efaktur_of_diskon(self):
        for record in self:
            record.efaktur_of_diskon = 0

    efaktur_of_diskon = fields.Char(
        string="OF_DISKON",
        compute="_compute_efaktur_of_diskon",
        store=True,
        compute_sudo=True,
    )

    @api.depends("price_subtotal")
    def _compute_efaktur_of_dpp(self):
        for record in self:
            record.efaktur_of_dpp = str(record.price_subtotal)

    efaktur_of_dpp = fields.Char(
        string="OF_DPP",
        compute="_compute_efaktur_of_dpp",
        store=True,
        compute_sudo=True,
    )

    @api.depends("price_tax")
    def _compute_efaktur_of_dpp_lain(self):
        """Back-compute the Coretax "OtherTaxBase" from the line's VAT.

        For a "DPP Nilai Lain" tax (e.g. ``DPP = 11/12 * price_unit *
        quantity``, ``PPN = DPP * 0.12``), the adjusted base is not
        exposed by any stored field -- it only exists as a local
        variable inside the tax's ``python_compute`` snippet. Dividing
        ``price_tax`` back by the VAT rate recovers it without needing
        to detect which tax scheme is in use: for a regular tax the
        result trivially equals ``efaktur_of_dpp`` too, since there
        ``DPP == TaxBase``.
        """
        for record in self:
            record.efaktur_of_dpp_lain = str(int(record.price_tax / 0.12))

    efaktur_of_dpp_lain = fields.Char(
        string="OF_DPP_LAIN",
        compute="_compute_efaktur_of_dpp_lain",
        store=True,
        compute_sudo=True,
    )

    @api.depends("price_tax")
    def _compute_efaktur_of_ppn(self):
        for record in self:
            record.efaktur_of_ppn = str(int(record.price_tax))

    efaktur_of_ppn = fields.Char(
        string="OF_PPN",
        compute="_compute_efaktur_of_ppn",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "product_id",
        "product_id.type",
    )
    def _compute_efaktur_of_opt(self):
        for record in self:
            result = False
            if record.product_id:
                if record.product_id.type == "service":
                    result = "B"
                else:
                    result = "A"
            record.efaktur_of_opt = result

    efaktur_of_opt = fields.Char(
        string="OF_OPT",
        compute="_compute_efaktur_of_opt",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "uom_id",
    )
    def _compute_efaktur_of_unit(self):
        for record in self:
            result = False
            if record.uom_id:
                result = record.uom_id.efaktur_code
            record.efaktur_of_unit = result

    efaktur_of_unit = fields.Char(
        string="OF_OPT",
        compute="_compute_efaktur_of_unit",
        store=True,
        compute_sudo=True,
    )
