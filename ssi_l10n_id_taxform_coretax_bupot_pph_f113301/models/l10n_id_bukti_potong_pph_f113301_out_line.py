# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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
            "Code's Tariff Type is TER; every other tariff regime "
            "(PS17/Harian/Pesangon/Pensiun) must be entered manually."
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
            "Coretax XML. Automatic (TER) or manual depending on "
            "Rate Computation."
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
        "bukti_potong_id.ptkp_category_id",
        "bukti_potong_id.date",
    )
    def _compute_rate(self):
        """Compute the withholding rate.

        Automatic computation only runs for the TER tariff type,
        looking up ``l10n_id.pph_21_ter`` with the header's PTKP
        category. It never raises: incomplete TER data (missing
        table/PTKP line) falls back to ``0.0`` here so a draft line
        can still be saved — the export step
        (``_prepare_coretax_bupot_line``) is what validates the rate
        is usable before the Coretax XML is generated.

        :return: nothing; assigns ``rate``
        """
        for line in self:
            result = line.manual_rate
            if (
                line.rate_computation_method == "auto"
                and line.coretax_tax_object_code.tariff_type == "ter"
            ):
                result = line._get_auto_ter_rate()
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

    @api.constrains(
        "rate_computation_method",
    )
    def _check_rate_computation_method(self):
        """Reject automatic rate computation outside the TER regime.

        :raises ValidationError: when ``rate_computation_method`` is
            ``auto`` on a line whose tax object is not tariff type
            TER
        """
        for line in self:
            if not line._check_rate_computation_method_condition():
                error_message = _(
                    """
Context: Set Rate Computation on a BP21 line
Database ID: %s
Problem: Automatic rate computation is only supported for the TER
tariff type, but the selected Coretax Tax Object Code is not TER
Solution: Select Manual and enter the rate by hand, or choose a tax
object code whose Tariff Type is TER
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
        return self.coretax_tax_object_code.tariff_type == "ter"
