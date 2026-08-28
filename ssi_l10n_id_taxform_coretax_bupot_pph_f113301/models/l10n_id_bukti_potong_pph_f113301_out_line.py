# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class L10nIdBuktiPotongPphF113301OutLine(models.Model):
    """Adds Coretax DPP/rate/reference-document data to a BP21 line.

    Every income item of an outgoing PPh 21/26 non-final withholding
    slip (form f.1.1.33.01, "BP21") maps to one Section B row of the
    Coretax XML: a tax facility, the DPP derived from the tax
    object's ``deemed`` factor, a withholding rate, and an optional
    reference document (invoice/contract) being reported on.
    """

    _name = "l10n_id.bukti_potong_pph_f113301_out_line"
    _inherit = [
        "l10n_id.bukti_potong_pph_f113301_out_line",
    ]

    fasilitas_pajak_id = fields.Many2one(
        string="Fasilitas Pajak",
        comodel_name="l10n_id.taxform_kode_fasilitas_pajak",
        ondelete="restrict",
        help=(
            "DGT tax facility applied to this income item, used as "
            "the ``TaxCertificate`` element of the Coretax XML. Left "
            "empty when no facility applies."
        ),
    )
    reference_document_type_id = fields.Many2one(
        string="Jenis Dokumen Referensi",
        comodel_name="l10n_id.taxform_jenis_dokumen_referensi",
        ondelete="restrict",
        help=(
            "Type of the source document (invoice, contract, etc.) "
            "this income item is reported against, used as the "
            "``Document`` element of the Coretax XML."
        ),
    )
    reference_document_number = fields.Char(
        string="Nomor Dokumen Referensi",
        help="Number of the reference document.",
    )
    reference_document_date = fields.Date(
        string="Tanggal Dokumen Referensi",
        help="Date of the reference document.",
    )
    dpp = fields.Float(
        string="DPP",
        compute="_compute_dpp",
        store=True,
        compute_sudo=True,
        help=(
            "Dasar Pengenaan Pajak: ``amount`` multiplied by the "
            "``deemed`` factor of the selected Coretax Tax Object "
            "Code (1.0 when the tax object has no deemed factor set)."
        ),
    )
    rate_computation_method = fields.Selection(
        string="Perhitungan Tarif",
        selection=[
            ("auto", "Otomatis"),
            ("manual", "Manual"),
        ],
        required=True,
        default="manual",
        help=(
            "Automatic is only supported when the Coretax Tax Object "
            "Code's Tariff Type is TER, PS17 (Pasal 17), or Final "
            "(Tarif Tetap per Kode Objek Pajak); every other tariff "
            "regime (Harian/Pesangon/Pensiun) must be entered manually."
        ),
    )
    manual_rate = fields.Float(
        string="Tarif (Manual)",
        help="Withholding rate entered manually, as a fraction (e.g. 0.05 for 5%).",
    )
    rate = fields.Float(
        string="Tarif",
        compute="_compute_rate",
        store=True,
        compute_sudo=True,
        help=(
            "Withholding rate used as the ``Rate`` element of the "
            "Coretax XML. Automatic (TER, PS17, or Final) or manual "
            "depending on Rate Computation."
        ),
    )
    amount_tax = fields.Float(
        string="Tax Amount",
        compute="_compute_amount_tax",
        store=True,
        compute_sudo=True,
        help=(
            "Withheld tax amount, computed as ``dpp`` multiplied by "
            "``rate`` — independent of ``tax_id``'s own percentage. "
            "``tax_id`` is only used to resolve the debit/credit "
            "account for this line."
        ),
    )

    @api.depends(
        "amount",
        "coretax_tax_object_code.deemed",
    )
    def _compute_dpp(self):
        """Derive the DPP from the withheld amount and the tax
        object's deemed factor.

        :return: nothing; assigns ``dpp``
        """
        for line in self:
            result = 0.0
            deemed = line.coretax_tax_object_code.deemed or 1.0
            result = line.amount * deemed
            line.dpp = result

    @api.depends(
        "rate_computation_method",
        "manual_rate",
        "dpp",
        "coretax_tax_object_code.tariff_type",
        "coretax_tax_object_code.fixed_rate",
        "bukti_potong_id.ptkp_category_id",
        "bukti_potong_id.date",
        "bukti_potong_id.wajib_pajak_id",
    )
    def _compute_rate(self):
        """Compute the withholding rate.

        Automatic computation runs for three tariff types: TER
        (looking up ``l10n_id.pph_21_ter`` with the header's PTKP
        category), PS17/Pasal 17 (looking up the cumulative-per-tax-
        year progressive bracket in ``l10n_id.pph_21_rate``), and
        Final/Tarif Tetap (taking the tax object's ``fixed_rate`` as
        is). It never raises: incomplete data (missing table/PTKP
        line, missing recipient) falls back to ``0.0`` here so a
        draft line can still be saved — the export step
        (``_prepare_coretax_bupot_line``) is what validates the rate
        is usable before the Coretax XML is generated.

        Note: this compute cannot react to changes on *other* BP21
        documents that alter the cumulative history (Odoo
        ``@api.depends`` does not reach cross-record ``search()``
        calls) — a known and accepted limitation, consistent with the
        practice that a ``done`` withholding slip is not
        retroactively recomputed when a new transaction arrives.

        :return: nothing; assigns ``rate``
        """
        for line in self:
            result = line.manual_rate
            tariff_type = line.coretax_tax_object_code.tariff_type
            if line.rate_computation_method == "auto" and tariff_type == "ter":
                result = line._get_auto_ter_rate()
            elif line.rate_computation_method == "auto" and tariff_type == "ps17":
                result = line._get_auto_ps17_rate()
            elif line.rate_computation_method == "auto" and tariff_type == "final_flat":
                result = line.coretax_tax_object_code.fixed_rate
            line.rate = result

    @api.depends(
        "income_move_line_ids",
        "income_move_line_ids.debit",
        "income_move_line_ids.credit",
        "amount_computation_method",
        "manual_amount",
    )
    def _compute_amount(self):
        """Override the mixin's ``_compute_amount`` to stop it from
        also assigning ``amount_tax``.

        ``amount`` and ``amount_tax`` share one compute method in the
        mixin (``ssi_l10n_id_taxform_bukti_potong_pph_mixin.models.
        l10n_id_bukti_potong_pph_line_mixin.
        L10nIdBuktiPotongPphLineMixin._compute_amount``), and that
        method's body unconditionally assigns ``line.amount_tax`` too
        (from ``line.tax_id.compute_all()``) as a direct side effect
        — not merely as a declared ``compute=``. Redeclaring
        ``amount_tax`` with a separate ``compute=`` elsewhere does
        not stop this: the mixin's method still runs (for ``amount``)
        and its direct assignment to ``amount_tax`` still overwrites
        whatever the separate compute produced.

        The only way to stop the side effect is to replace the
        method's body for this model. This override therefore
        **duplicates** the mixin's ``amount``-only logic verbatim
        (same ``@api.depends``, same branches) and simply omits the
        ``amount_tax``-related statements — it deliberately does NOT
        call ``super()``, since doing so would re-run the very
        ``tax_id.compute_all()`` side effect this override exists to
        remove. ``amount_tax`` is computed independently by
        ``_compute_amount_tax`` below.

        Kept deliberately WITHOUT ``dpp``/``rate`` in
        ``@api.depends``: adding either here would depend ``amount``
        (this field) on ``dpp``, whose own compute (``_compute_dpp``)
        already depends on ``amount`` — a circular dependency that
        made Odoo's recompute silently stall on ``0.0`` for ``dpp``,
        ``rate``, and ``amount_tax`` alike (observed in CI, not just
        theorised).

        :return: nothing; assigns ``amount``
        """
        for line in self:
            result = 0.0
            if line.amount_computation_method == "auto":
                for move_line in line.income_move_line_ids:
                    if line.bukti_potong_id.direction == "in":
                        result += move_line.credit
                    else:
                        result += move_line.debit
            else:
                result = line.manual_amount
            line.amount = result

    @api.depends(
        "dpp",
        "rate",
        "amount",
        "tax_id",
    )
    def _compute_amount_tax(self):
        """Compute the withheld tax amount, preferring DPP x rate but
        falling back to ``tax_id.compute_all()`` for legacy lines.

        ``amount_tax`` comes from ``dpp`` multiplied by ``rate``
        **only when both are positive** — i.e. only for lines that
        actually went through the Coretax DPP/Tarif configuration
        added by this module. Lines created through the pre-existing
        flow of ``l10n_id.bukti_potong_pph_f113301_out_line`` (e.g.
        ``ssi_l10n_id_taxform_bukti_potong_pph_f113301`` demo/tour
        fixtures, which predate this module and never populate
        ``coretax_tax_object_code``/``manual_rate``) leave ``rate``
        at its default ``0.0``: applying the ``dpp`` x ``rate``
        formula unconditionally would silently zero out their
        ``amount_tax`` and trip
        ``_constrains_total_tax_final``\\ 's "Total tax has to be
        greater than 0" on documents that were valid before this
        module's ``dpp``/``rate`` fields existed. For those, this
        falls back to the mixin's original computation (``tax_id``
        applied on ``amount``) so pre-existing data keeps working
        unmodified — an explicit, user-confirmed design decision
        (see issue #232 discussion), not an inference of this
        method.

        :return: nothing; assigns ``amount_tax``
        """
        for line in self:
            result = 0.0
            if line.dpp > 0.0 and line.rate > 0.0:
                currency = line.bukti_potong_id.company_id.currency_id
                result = currency.round(line.dpp * line.rate)
            elif line.amount != 0.0:
                taxes = line.tax_id.compute_all(
                    line.amount,
                    line.bukti_potong_id.company_id.currency_id,
                    1.0,
                    product=False,
                    partner=False,
                )
                result = taxes["total_included"] - taxes["total_excluded"]
            line.amount_tax = result

    def _get_auto_ter_rate(self):
        """Look up the TER rate for this line's DPP and header PTKP
        category.

        :return: the TER rate as a fraction, or ``0.0`` when the TER
            table or PTKP category is not (yet) configured
        """
        self.ensure_one()
        ptkp_category = self.bukti_potong_id.ptkp_category_id
        if not ptkp_category:
            return 0.0
        try:
            ter = self.env["l10n_id.pph_21_ter"].find(self.bukti_potong_id.date)
            return ter.compute_tax(self.dpp, [ptkp_category.id])["rate"]
        except ValidationError:
            return 0.0

    def _get_auto_ps17_rate(self):
        """Look up the effective PS17 (Pasal 17) progressive rate for
        this line, cumulative per recipient per tax year.

        Bukan Pegawai (non-employee) recipients paid repeatedly by the
        same withholder within a tax year are taxed on their
        cumulative DPP: the bracket that applies to a given
        transaction depends on how much has already been withheld for
        that recipient this year, not on this transaction's DPP alone.
        This method derives the effective rate as the marginal tax
        (tax on cumulative DPP after this line, minus tax on
        cumulative DPP before it) divided by this line's own DPP, so
        the result is correct even when the transaction straddles a
        bracket boundary.

        :return: the effective PS17 rate as a fraction, or ``0.0``
            when the recipient/document date is not (yet) set, the
            PPh 21 Rate table is not configured for the document
            date, or this line's DPP is not positive
        """
        self.ensure_one()
        wajib_pajak = self.bukti_potong_id.wajib_pajak_id
        doc_date = self.bukti_potong_id.date
        if not wajib_pajak or not doc_date:
            return 0.0
        if self.dpp <= 0:
            return 0.0
        previous_lines = self.search(
            self._get_ps17_cumulative_criteria(wajib_pajak, doc_date)
        )
        cumulative_before = sum(previous_lines.mapped("dpp"))
        cumulative_after = cumulative_before + self.dpp
        try:
            rate_record = self.env["l10n_id.pph_21_rate"].find(doc_date)
        except ValidationError:
            return 0.0
        tax_before = rate_record.compute_tax(cumulative_before)
        tax_after = rate_record.compute_tax(cumulative_after)
        return (tax_after - tax_before) / self.dpp

    def _get_ps17_cumulative_criteria(self, wajib_pajak, doc_date):
        """Build the domain selecting this recipient's other PS17
        lines already accounted for in the current tax year.

        Only ``done`` documents are counted (draft/cancel/reject are
        excluded), and this line itself is always excluded so a line
        being edited (typically still draft) never counts itself as
        part of its own cumulative-before amount.

        :param wajib_pajak: recipient (``res.partner``) whose PS17
            lines are being accumulated
        :param doc_date: document date used to derive the tax year
        :return: a ``search()`` domain (list of tuples)
        """
        return [
            ("bukti_potong_id.wajib_pajak_id", "=", wajib_pajak.id),
            ("bukti_potong_id.date", ">=", date(doc_date.year, 1, 1)),
            ("bukti_potong_id.date", "<=", date(doc_date.year, 12, 31)),
            ("bukti_potong_id.state", "=", "done"),
            ("coretax_tax_object_code.tariff_type", "=", "ps17"),
            ("id", "!=", self.id),
        ]

    @api.constrains(
        "rate_computation_method",
    )
    def _check_rate_computation_method(self):
        """Reject automatic rate computation outside the supported
        tariff regimes.

        :raises ValidationError: when ``rate_computation_method`` is
            ``auto`` on a line whose tax object is none of TER, PS17
            (Pasal 17), or Final (Tarif Tetap per Kode Objek Pajak)
        """
        for line in self:
            if not line._check_rate_computation_method_condition():
                error_message = _(
                    """
Context: Set Rate Computation on a BP21 line
Database ID: %s
Problem: Automatic rate computation is only supported for the TER,
PS17 (Pasal 17), and Final (Tarif Tetap per Kode Objek Pajak) tariff
types, but the selected Coretax Tax Object Code is none of these
Solution: Select Manual and enter the rate by hand, or choose a tax
object code whose Tariff Type is TER, PS17, or Final
"""
                    % (line.id,)
                )
                raise ValidationError(error_message)

    def _check_rate_computation_method_condition(self):
        """Tell whether ``rate_computation_method`` is consistent with
        the selected tax object's tariff type.

        :return: True when valid; never raises
        """
        self.ensure_one()
        if self.rate_computation_method != "auto":
            return True
        return self.coretax_tax_object_code.tariff_type in (
            "ter",
            "final_flat",
            "ps17",
        )
