# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class L10nIdBuktiPotongPphF113301Out(models.Model):
    """Adds the BP21-specific Coretax fields and the enriched Coretax
    XML export to the PPh 21/26 non-final withholding slip.

    Extends the generic ``action_export_coretax_bupot_pph_out_xml``
    (from ``ssi_l10n_id_taxform_coretax_bupot_pph_out``) with the
    withholding date, PTKP status, and recipient identity data that
    the DGT Coretax schema requires for BP21 (form f.1.1.33.01), by
    overriding ``_get_coretax_bupot_pph_out_template_xmlid`` and the
    ``_prepare_coretax_bupot_*`` extension points rather than
    changing the base export shared by other bukti potong types.
    """

    _name = "l10n_id.bukti_potong_pph_f113301_out"
    _inherit = [
        "l10n_id.bukti_potong_pph_f113301_out",
    ]

    @api.model
    def _default_withholding_date(self):
        """Return today's date as the default withholding date.

        :return: today's date, formatted ``%Y-%m-%d``
        """
        return self._default_date()

    withholding_date = fields.Date(
        string="Tanggal Pemotongan",
        required=True,
        default=lambda self: self._default_withholding_date(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "Actual date the tax was withheld, used as the "
            "``WithholdingDate`` element of the Coretax XML. Not "
            "always the same as Date (the document date)."
        ),
    )
    ptkp_category_id = fields.Many2one(
        string="Status PTKP",
        comodel_name="l10n_id.ptkp_category",
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "PTKP status of the wajib pajak, used as the "
            "``StatusTaxExemption`` element of the Coretax XML and "
            "as the PTKP lookup key for automatic TER rate "
            "computation on this document's lines."
        ),
    )

    id_tku_penerima = fields.Char(
        string="ID TKU Penerima",
        related="wajib_pajak_id.nitku",
        store=False,
        compute_sudo=True,
        help=(
            "NITKU of the wajib pajak (income recipient), used as the "
            "``IDPlaceOfBusinessActivityOfIncomeRecipient`` element of "
            "the Coretax XML. Set on the Wajib Pajak partner record."
        ),
    )
    id_tku_pemotong = fields.Char(
        string="ID TKU Pemotong",
        related="pemotong_pajak_id.nitku",
        store=False,
        compute_sudo=True,
        help=(
            "NITKU of the pemotong pajak (withholder), used as the "
            "``IDPlaceOfBusinessActivity`` element of the Coretax XML. "
            "Set on the Pemotong Pajak partner record."
        ),
    )

    @api.onchange(
        "date",
    )
    def onchange_withholding_date(self):
        """Default ``withholding_date`` from ``date``.

        Mirrors the base mixin's ``onchange_tax_period``: the
        withholding date follows the document date until the user
        overrides it manually after picking the date.
        """
        self.withholding_date = self.date

    def _get_coretax_bupot_pph_out_template_xmlid(self):
        """Render the BP21-specific Coretax template instead of the
        base ``MmWithholding`` template.

        :return: full XML ID of the ``coretax_bupot_pph_f113301_out``
            template
        """
        self.ensure_one()
        return "ssi_l10n_id_taxform_coretax_bupot_pph_f113301.xml"

    def _prepare_coretax_bupot_pph_out_values(self):
        """Validate the BP21-specific header data, then delegate to
        the base implementation for the pemotong/wajib pajak checks
        and the per-line values.

        :raises UserError: when ``ptkp_category_id`` or
            ``withholding_date`` is not set
        :return: the rendering context built by the base
            implementation
        """
        self.ensure_one()
        if not self.ptkp_category_id or not self.withholding_date:
            missing = (
                not self.ptkp_category_id and "PTKP Category" or "Withholding Date"
            )
            error_message = _(
                """
Context: Generate Coretax BP21 (f.1.1.33.01) Out XML
Database ID: %s
Problem: This document has no %s configured
Solution: Set the PTKP Category and Withholding Date before exporting
"""
                % (self.id, missing)
            )
            raise UserError(error_message)
        _super = super()
        return _super._prepare_coretax_bupot_pph_out_values()

    def _prepare_coretax_bupot_line(self, line):
        """Enrich the base line values with the BP21-specific Coretax
        elements (facility, deemed, rate, reference document,
        recipient TKU, withholding date).

        :param line: a ``l10n_id.bukti_potong_pph_f113301_out_line``
            record
        :return: dict of rendering values for one ``MmWithholding``
            element, or ``False`` when the base implementation
            excludes this line (mis. zero withheld tax)
        """
        self.ensure_one()
        _super = super()
        result = _super._prepare_coretax_bupot_line(line)
        if not result:
            return result
        document_date = ""
        if line.reference_document_date:
            document_date = fields.Date.to_string(line.reference_document_date)
        result.update(
            {
                "status_tax_exemption": self.ptkp_category_id.code or "",
                "tax_certificate": line.fasilitas_pajak_id.code or "N/A",
                "deemed": self._coretax_format_number(
                    line.coretax_tax_object_code.deemed or 1.0
                ),
                "rate": self._coretax_format_number(line.rate),
                "document_type": line.reference_document_type_id.code or False,
                "document_number": line.reference_document_number or "",
                "document_date": document_date,
                "id_place_of_business_activity_of_income_recipient": (
                    self.id_tku_penerima or ""
                ),
                "withholding_date": fields.Date.to_string(self.withholding_date),
            }
        )
        return result
