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

    def _all_lines_auto_computed(self):
        """Tell whether every active line of this document went
        through an automatic Coretax tariff lookup with a known
        tariff type.

        An "active" line is one whose ``amount`` is not zero — an
        empty/unfilled line is not considered when deciding whether
        the document as a whole is fully automatic. A document with
        no active lines at all (e.g. a brand-new, still-empty
        document) is **not** exempted: it returns ``False`` so the
        base "Total tax has to be greater than 0" rule keeps applying
        to it exactly as before.

        The check is intentionally "all active lines", not "at least
        one" — a per-user-confirmed design decision (see issue #245
        discussion) — so a document mixing a legitimate 0%-tariff
        auto line with a manual line whose rate has simply not been
        filled in yet still fails validation as before.

        :return: ``True`` when this document has at least one active
            line and every active line is
            ``rate_computation_method == "auto"`` with a Coretax Tax
            Object Code Tariff Type in ``ter``, ``final_flat``,
            ``ps17``, ``harian``, ``pesangon``, or ``pensiun``;
            ``False`` otherwise
        """
        self.ensure_one()
        active_lines = self.line_ids.filtered(lambda ln: ln.amount != 0.0)
        if not active_lines:
            return False
        known_tariff_types = (
            "ter",
            "final_flat",
            "ps17",
            "harian",
            "pesangon",
            "pensiun",
        )
        return all(
            line.rate_computation_method == "auto"
            and line.coretax_tax_object_code.tariff_type in known_tariff_types
            for line in active_lines
        )

    @api.constrains(
        "total_tax_final",
    )
    def _constrains_total_tax_final(self):
        """Override the mixin's constraint to exempt documents whose
        active lines are entirely auto-computed with a known tariff
        type.

        The base rule (``ssi_l10n_id_taxform_bukti_potong_pph_mixin``)
        treats ``total_tax_final <= 0.0`` on a non-empty document as
        incomplete data — reasonable for manual rate entry, since a
        rate of ``0.0`` there almost always means "not filled in
        yet". It is wrong for the Coretax automatic tariff lookups
        added by this module: several tariff types (TER/Harian below
        their threshold, or Pesangon/Pensiun at/under their exempt
        bracket) legitimately resolve to a 0% rate, and a document
        made up entirely of such lines has a genuinely correct
        ``total_tax_final`` of ``0.0``.

        This override replaces the base method's body outright
        (rather than extending it with ``super()``): the base method
        lives in another module's mixin model, so there is no
        narrower hook to attach to — the same reasoning documented on
        ``L10nIdBuktiPotongPphF113301OutLine._compute_amount``.

        :raises UserError: when ``total_tax_final`` is not greater
            than zero while ``line_ids`` is not empty, unless every
            active line is auto-computed with a known tariff type
            (see ``_all_lines_auto_computed``)
        """
        for record in self:
            if (
                record.total_tax_final <= 0.0
                and len(record.line_ids) > 0
                and not record._all_lines_auto_computed()
            ):
                raise UserError(_("Total tax has to be greater than 0"))

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
