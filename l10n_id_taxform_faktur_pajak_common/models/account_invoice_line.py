# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _name = "account.invoice.line"
    _inherit = "account.invoice.line"

    @api.depends(
        "product_id",
    )
    @api.multi
    def _compute_kode_objek(self):
        for line in self:
            line.enofa_kode_objek = (
                line.product_id and line.product_id.default_code or "-"
            )

    enofa_kode_objek = fields.Char(
        string="KODE_OBJEK",
        compute="_compute_kode_objek",
        store=False,
    )

    @api.depends(
        "name",
    )
    @api.multi
    def _compute_nama(self):
        for line in self:
            line.enofa_nama = line.name or "-"

    enofa_nama = fields.Char(
        string="NAMA",
        compute="_compute_nama",
        store=False,
    )

    @api.depends(
        "price_unit",
        "quantity",
        "invoice_line_tax_ids",
    )
    @api.multi
    def _compute_harga_satuan(self):
        for line in self:
            line.enofa_harga_satuan = line.price_unit

    enofa_harga_satuan = fields.Char(
        string="HARGA_SATUAN",
        compute="_compute_harga_satuan",
        store=False,
    )

    @api.depends(
        "quantity",
    )
    @api.multi
    def _compute_jumlah_barang(self):
        for line in self:
            line.enofa_jumlah_barang = line.quantity

    enofa_jumlah_barang = fields.Char(
        string="JUMLAH_BARANG",
        compute="_compute_jumlah_barang",
        store=False,
    )

    @api.depends(
        "price_unit",
        "quantity",
        "invoice_line_tax_ids",
    )
    @api.multi
    def _compute_harga_total(self):
        for line in self:
            line.enofa_harga_total = line.price_subtotal

    enofa_harga_total = fields.Char(
        string="HARGA_TOTAL",
        compute="_compute_harga_total",
        store=False,
    )

    @api.multi
    def _compute_diskon(self):
        for line in self:
            line.enofa_diskon = 0.0

    enofa_diskon = fields.Char(
        string="DISKON",
        compute="_compute_diskon",
        store=False,
    )

    @api.depends(
        "price_unit",
        "quantity",
        "invoice_line_tax_ids",
    )
    @api.multi
    def _compute_dpp(self):
        for line in self:
            line.enofa_dpp = line.price_subtotal

    enofa_dpp = fields.Char(
        string="DPP",
        compute="_compute_dpp",
        store=False,
    )

    @api.depends(
        "price_unit",
        "quantity",
        "invoice_line_tax_ids",
    )
    @api.multi
    def _compute_ppn(self):
        for line in self:
            line.enofa_ppn = line.price_total - line.price_subtotal

    enofa_ppn = fields.Char(
        string="PPN",
        compute="_compute_ppn",
        store=False,
    )

    @api.depends(
        "price_unit",
        "quantity",
        "invoice_line_tax_ids",
    )
    @api.multi
    def _compute_tarif_ppnbm(self):
        for line in self:
            line.enofa_tarif_ppnbm = 0.0

    enofa_tarif_ppnbm = fields.Char(
        string="TARIF_PPNBM",
        compute="_compute_tarif_ppnbm",
        store=False,
    )

    @api.depends(
        "price_unit",
        "quantity",
        "invoice_line_tax_ids",
    )
    @api.multi
    def _compute_ppnbm(self):
        for line in self:
            line.enofa_ppnbm = 0.0

    enofa_ppnbm = fields.Char(
        string="PPNBM",
        compute="_compute_ppnbm",
        store=False,
    )
