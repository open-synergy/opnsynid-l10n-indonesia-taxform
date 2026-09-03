# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.models import NewId


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
            "Automatic is supported for every Coretax Tax Object Code "
            "Tariff Type (TER, PS17/Pasal 17, Harian, Pesangon, "
            "Pensiun, or Final/Tarif Tetap per Kode Objek Pajak). "
            "Left empty on the tax object code, Manual is the only "
            "option."
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

        Automatic computation runs for every supported tariff type:
        TER (looking up ``l10n_id.pph_21_ter`` with the header's PTKP
        category), PS17/Pasal 17 (a nominal UU HPP bracket lookup on
        the cumulative-per-tax-year DPP, see
        ``_get_ps17_bracket_rate``), Final/Tarif Tetap (taking the
        tax object's ``fixed_rate`` as is), and Harian/Pesangon/
        Pensiun (a non-cumulative, per-line bracket lookup on this
        line's own ``dpp`` — see ``_get_harian_bracket_rate``,
        ``_get_pesangon_bracket_rate``, ``_get_pensiun_bracket_rate``).
        It never raises: incomplete data (missing PTKP line, missing
        recipient) falls back to ``0.0`` here so a draft line can
        still be saved — the export step
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
            elif line.rate_computation_method == "auto" and tariff_type == "harian":
                result = line._get_harian_bracket_rate(line.dpp)
            elif line.rate_computation_method == "auto" and tariff_type == "pesangon":
                result = line._get_pesangon_bracket_rate(line.dpp)
            elif line.rate_computation_method == "auto" and tariff_type == "pensiun":
                result = line._get_pensiun_bracket_rate(line.dpp)
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
        "coretax_tax_object_code.tariff_type",
        "rate_computation_method",
    )
    def _compute_amount_tax(self):
        """Compute the withheld tax amount, preferring DPP x rate but
        falling back to ``tax_id.compute_all()`` for legacy lines.

        Three branches, checked in order:

        1. **PS17 (Pasal 17), automatic.** ``amount_tax`` comes from
           ``_get_auto_ps17_tax_amount()`` — the marginal tax on the
           recipient's cumulative DPP — **not** ``dpp`` x ``rate``.
           This module's ``rate`` for PS17 lines is now the nominal
           bracket rate (see ``_get_ps17_bracket_rate``), which is a
           single-layer lookup and would silently under/over-state
           the tax for any DPP that straddles more than one bracket.
        2. **Everything else with a positive ``dpp``/``rate``.**
           ``amount_tax`` is ``dpp`` multiplied by ``rate`` — i.e.
           lines that went through the Coretax DPP/Tarif
           configuration added by this module (TER, Final, or manual
           rate entry).
        3. **Legacy fallback.** Lines created through the
           pre-existing flow of
           ``l10n_id.bukti_potong_pph_f113301_out_line`` (e.g.
           ``ssi_l10n_id_taxform_bukti_potong_pph_f113301`` demo/tour
           fixtures, which predate this module and never populate
           ``coretax_tax_object_code``/``manual_rate``) leave
           ``rate`` at its default ``0.0``: applying the ``dpp`` x
           ``rate`` formula unconditionally would silently zero out
           their ``amount_tax`` and trip
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
            tariff_type = line.coretax_tax_object_code.tariff_type
            if (
                line.rate_computation_method == "auto"
                and tariff_type == "ps17"
                and line.dpp > 0.0
            ):
                currency = line.bukti_potong_id.company_id.currency_id
                result = currency.round(line._get_auto_ps17_tax_amount())
            elif line.dpp > 0.0 and line.rate > 0.0:
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

        ``Pph21TerLine.compute_tax()`` returns ``rate`` as a raw
        percentage (e.g. ``6.0`` for 6%, matching the ``pph_rate``
        bracket field it is read from) rather than a fraction, so the
        result is divided by 100 here to match this module's own
        ``rate`` convention (a fraction, e.g. ``0.06`` for 6% — see
        ``manual_rate``/``fixed_rate``/``_get_ps17_bracket_rate``).

        :return: the TER rate as a fraction, or ``0.0`` when the TER
            table or PTKP category is not (yet) configured
        """
        self.ensure_one()
        ptkp_category = self.bukti_potong_id.ptkp_category_id
        if not ptkp_category:
            return 0.0
        try:
            ter = self.env["l10n_id.pph_21_ter"].find(self.bukti_potong_id.date)
            return ter.compute_tax(self.dpp, [ptkp_category.id])["rate"] / 100.0
        except ValidationError:
            return 0.0

    def _get_auto_ps17_rate(self):
        """Look up the nominal PS17 (Pasal 17) bracket rate for this
        line, cumulative per recipient per tax year.

        Bukan Pegawai (non-employee) recipients paid repeatedly by the
        same withholder within a tax year are taxed on their
        cumulative DPP: the bracket that applies to a given
        transaction depends on how much has already been withheld for
        that recipient this year, not on this transaction's DPP
        alone. This method returns the nominal rate of the highest
        bracket touched by the cumulative DPP *after* this line
        (``_get_ps17_bracket_rate``) — a single-layer lookup, not an
        averaged/blended rate — so a DPP that straddles more than one
        bracket still shows one of the five official rates
        (5/15/25/30/35%) rather than a value in between. The actual
        withheld tax amount is computed separately, by
        ``_get_auto_ps17_tax_amount``.

        :return: the nominal PS17 bracket rate as a fraction (see
            ``_get_ps17_bracket_rate``), or ``0.0`` when the
            recipient/document date is not (yet) set, or this line's
            DPP is not positive
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
        return self._get_ps17_bracket_rate(cumulative_after)

    @api.model
    def _get_ps17_bracket_rate(self, cumulative_dpp):
        """Look up the nominal PS17 (Pasal 17) rate for a cumulative
        DPP, as a plain single-layer bracket lookup.

        Mirrors the ``Rate`` formula of the client's Coretax
        submission tool proven valid for XML submission (``BP21
        Excel to XML v.4.xlsx``, sheet DATA, column W formula)::

            IF(R<=60000000,5,
              IF(R<=250000000,15,
                IF(R<=500000000,25,
                  IF(R<=5000000000,30,35))))

        This is a lookup of the highest UU HPP Pasal 17 layer touched
        by ``cumulative_dpp`` — it does **not** average/blend the
        rates of the layers below it.

        :param cumulative_dpp: cumulative taxable income (DPP) for
            the recipient's tax year, including the transaction being
            rated
        :return: the nominal bracket rate as a fraction, one of
            ``0.05``, ``0.15``, ``0.25``, ``0.30``, or ``0.35``
        """
        if cumulative_dpp <= 60000000.0:
            return 0.05
        elif cumulative_dpp <= 250000000.0:
            return 0.15
        elif cumulative_dpp <= 500000000.0:
            return 0.25
        elif cumulative_dpp <= 5000000000.0:
            return 0.30
        else:
            return 0.35

    @api.model
    def _get_harian_bracket_rate(self, dpp):
        """Look up the nominal Harian (daily wage) bracket rate for a
        single line's DPP.

        Mirrors the ``Rate`` formula of the client's Coretax
        submission tool proven valid for XML submission (``BP21
        Excel to XML v.4.xlsx``, sheet DATA, column X). Unlike PS17,
        this is **not** cumulative across documents: only this
        line's own ``dpp`` is used.

        :param dpp: taxable income (DPP) of this line
        :return: the nominal bracket rate as a fraction, ``0.0`` or
            ``0.005``
        """
        if dpp <= 450000.0:
            return 0.0
        elif dpp <= 2500000.0:
            return 0.005
        else:
            return 0.0

    @api.model
    def _get_pesangon_bracket_rate(self, dpp):
        """Look up the nominal Pesangon (severance pay) bracket rate
        for a single line's DPP.

        Mirrors the ``Rate`` formula of the client's Coretax
        submission tool proven valid for XML submission (``BP21
        Excel to XML v.4.xlsx``, sheet DATA, column Y). Unlike PS17,
        this is **not** cumulative across documents: only this
        line's own ``dpp`` is used.

        :param dpp: taxable income (DPP) of this line
        :return: the nominal bracket rate as a fraction, one of
            ``0.0``, ``0.05``, ``0.15``, or ``0.25``
        """
        if dpp <= 50000000.0:
            return 0.0
        elif dpp <= 100000000.0:
            return 0.05
        elif dpp <= 500000000.0:
            return 0.15
        else:
            return 0.25

    @api.model
    def _get_pensiun_bracket_rate(self, dpp):
        """Look up the nominal Pensiun (pension) bracket rate for a
        single line's DPP.

        Mirrors the ``Rate`` formula of the client's Coretax
        submission tool proven valid for XML submission (``BP21
        Excel to XML v.4.xlsx``, sheet DATA, column Z). Unlike PS17,
        this is **not** cumulative across documents: only this
        line's own ``dpp`` is used.

        :param dpp: taxable income (DPP) of this line
        :return: the nominal bracket rate as a fraction, ``0.0`` or
            ``0.05``
        """
        if dpp <= 50000000.0:
            return 0.0
        else:
            return 0.05

    def _get_auto_ps17_tax_amount(self):
        """Compute the PS17 (Pasal 17) withheld tax amount as the
        marginal tax on this line's cumulative DPP.

        Re-derives the recipient's cumulative-before/cumulative-after
        DPP the same way ``_get_auto_ps17_rate`` does. The two
        methods deliberately duplicate this lookup instead of sharing
        one return value: ``_compute_rate`` and ``_compute_amount_tax``
        are two independent compute methods with their own
        ``@api.depends``, and merging them would create an implicit
        coupling between computes. The tax amount itself still comes
        from ``l10n_id.pph_21_rate.compute_tax()`` (the progressive
        table configured for the document date) — independent of the
        nominal bracket ``rate`` shown to the user by
        ``_get_ps17_bracket_rate``.

        :return: the withheld tax amount (tax on cumulative DPP after
            this line, minus tax on cumulative DPP before it), or
            ``0.0`` when the recipient/document date is not (yet)
            set, the PPh 21 Rate table is not configured for the
            document date, or this line's DPP is not positive
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
        return tax_after - tax_before

    def _get_ps17_cumulative_criteria(self, wajib_pajak, doc_date):
        """Build the domain selecting this recipient's other PS17
        lines already accounted for in the current tax year.

        Only ``done`` documents are counted (draft/cancel/reject are
        excluded). This line itself is excluded by id **only when it
        is already saved** (``self.id`` is a real integer, not an
        ``odoo.models.NewId``): a plain ``("id", "!=", self.id)``
        crashes ``search()`` at the SQL level for an unsaved line
        (``self.id`` is a ``NewId``, not an integer, e.g. during an
        onchange in the form before the record is saved). Dropping
        the exclusion for unsaved lines is safe — the domain already
        restricts to ``state == "done"``, and an unsaved/new line can
        never be ``done``, so it could never have matched its own
        exclusion clause anyway.

        :param wajib_pajak: recipient (``res.partner``) whose PS17
            lines are being accumulated
        :param doc_date: document date used to derive the tax year
        :return: a ``search()`` domain (list of tuples)
        """
        domain = [
            ("bukti_potong_id.wajib_pajak_id", "=", wajib_pajak.id),
            ("bukti_potong_id.date", ">=", date(doc_date.year, 1, 1)),
            ("bukti_potong_id.date", "<=", date(doc_date.year, 12, 31)),
            ("bukti_potong_id.state", "=", "done"),
            ("coretax_tax_object_code.tariff_type", "=", "ps17"),
        ]
        if not isinstance(self.id, NewId):
            domain.append(("id", "!=", self.id))
        return domain

    @api.constrains(
        "rate_computation_method",
    )
    def _check_rate_computation_method(self):
        """Reject automatic rate computation when no tariff regime is
        set on the tax object.

        :raises ValidationError: when ``rate_computation_method`` is
            ``auto`` on a line whose tax object has no Tariff Type
            selected
        """
        for line in self:
            if not line._check_rate_computation_method_condition():
                error_message = _(
                    """
Context: Set Rate Computation on a BP21 line
Database ID: %s
Problem: Automatic rate computation requires the selected Coretax Tax
Object Code to have a Tariff Type (TER, PS17/Pasal 17, Harian,
Pesangon, Pensiun, or Final/Tarif Tetap per Kode Objek Pajak), but
none is set
Solution: Select Manual and enter the rate by hand, or choose a tax
object code with a Tariff Type set
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
            "harian",
            "pesangon",
            "pensiun",
        )
