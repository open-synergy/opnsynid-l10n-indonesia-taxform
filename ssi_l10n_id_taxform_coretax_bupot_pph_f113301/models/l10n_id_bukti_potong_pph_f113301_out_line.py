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
