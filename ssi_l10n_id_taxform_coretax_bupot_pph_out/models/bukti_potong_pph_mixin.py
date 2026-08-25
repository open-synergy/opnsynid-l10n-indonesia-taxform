# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64

from odoo import _, fields, models
from odoo.exceptions import UserError


class BuktiPotongPPhMixin(models.AbstractModel):
    """Adds Coretax XML export to an outgoing Bukti Potong PPh document.

    Builds the DGT Coretax ``MmWithholding`` XML from the withholder
    (``pemotong_pajak_id``), the wajib pajak, and each line with a
    positive tax amount, then exposes it through
    ``action_export_coretax_bupot_pph_out_xml`` as a downloadable
    ``ir.attachment``.
    """

    _inherit = "l10n_id.bukti_potong_pph_mixin"

    def _coretax_format_number(self, value):
        """Render a numeric value without a trailing ``.0`` so that integer
        amounts are written as plain integers in the XML."""
        if value == int(value):
            return str(int(value))
        return repr(float(value))

    def _get_coretax_pemotong(self):
        """Return the withholder NPWP (TIN) and NITKU (IDPlaceOfBusinessActivity).

        Both are taken from ``pemotong_pajak_id``: ``vat`` for the NPWP and
        ``nitku`` for the ID TKU."""
        self.ensure_one()
        partner = self.pemotong_pajak_id
        tin = (partner.vat or "").strip()
        id_tku = (partner.nitku or "").strip()
        if not tin or not id_tku:
            error_message = _(
                """
Context: Generate Coretax Bukti Potong PPh Out XML
Database ID: %s
Problem: The withholder "%s" has no %s configured
Solution: Set the NPWP (Tax ID) and NITKU of the withholder partner
"""
                % (
                    self.id,
                    partner.display_name,
                    not tin and "NPWP (Tax ID)" or "NITKU (ID TKU)",
                )
            )
            raise UserError(error_message)
        return tin, id_tku

    def _prepare_coretax_bupot_line(self, line):
        """Build the dict for one ``MmWithholding`` element from a bukti potong
        line. Returns ``False`` when the tax amount is not greater than zero."""
        self.ensure_one()
        if line.amount_tax <= 0.0:
            return False

        wajib_pajak = self.wajib_pajak_id
        tin = (wajib_pajak.vat or "").strip()
        if not tin:
            error_message = _(
                """
Context: Generate Coretax Bukti Potong PPh Out XML
Database ID: %s
Problem: Wajib pajak "%s" has no NPWP (Tax ID) configured
Solution: Set the NPWP of the wajib pajak partner
"""
                % (self.id, wajib_pajak.display_name)
            )
            raise UserError(error_message)

        indonesia = self.env.ref("base.id", raise_if_not_found=False)
        is_domestic = not wajib_pajak.country_id or (
            indonesia and wajib_pajak.country_id == indonesia
        )
        counterpart_opt = "Resident" if is_domestic else "NonResident"

        return {
            "tax_period_month": self.tax_period_id.date_start.month,
            "tax_period_year": self.tax_period_id.date_start.year,
            "counterpart_opt": counterpart_opt,
            "counterpart_tin": tin,
            "tax_object_code": line.coretax_tax_object_code.code or "",
            "gross": self._coretax_format_number(line.amount),
            "withholding_tax": self._coretax_format_number(line.amount_tax),
            "withholding_date": fields.Date.to_string(self.date),
        }

    def _prepare_coretax_bupot_pph_out_values(self):
        """Build the full rendering context for the Coretax Bukti Potong PPh
        Out XML: the withholder header plus one entry per line with a positive
        tax amount. Raises a ``UserError`` when required data is missing."""
        self.ensure_one()
        tin, id_tku = self._get_coretax_pemotong()

        lines = []
        for line in self.line_ids:
            line_data = self._prepare_coretax_bupot_line(line)
            if line_data:
                line_data["id_place_of_business_activity"] = id_tku
                lines.append(line_data)

        if not lines:
            error_message = _(
                """
Context: Generate Coretax Bukti Potong PPh Out XML
Database ID: %s
Problem: No line in this bukti potong has PPh withheld (greater than zero)
Solution: Add lines with a non-zero tax amount before exporting
"""
                % (self.id,)
            )
            raise UserError(error_message)

        return {
            "company_tin": tin,
            "company_id_tku": id_tku,
            "lines": lines,
        }

    def _get_coretax_bupot_pph_out_template_xmlid(self):
        """Return the XML ID of the QWeb template used to render the
        Coretax export.

        Extension point: override in a glue module (mis. the f113301
        BP21 module) to render a richer template without changing the
        export button or the base rendering context for other bukti
        potong types.

        :return: full XML ID of a ``qweb`` template record
        """
        self.ensure_one()
        return "ssi_l10n_id_taxform_coretax_bupot_pph_out.coretax_bupot_pph_out"

    def action_export_coretax_bupot_pph_out_xml(self):
        """Generate the Coretax XML file for this outgoing bukti potong PPh,
        attach it to the record, and return a download URL action."""
        self.ensure_one()
        values = self._prepare_coretax_bupot_pph_out_values()
        xml_bytes = self.env["ir.qweb"]._render(
            self._get_coretax_bupot_pph_out_template_xmlid(),
            values,
        )
        xml_content = b'<?xml version="1.0" encoding="UTF-8"?>\n' + xml_bytes
        attachment = self.env["ir.attachment"].create(
            {
                "name": "coretax_bupot_pph_%s.xml" % (self.name or self.id),
                "type": "binary",
                "datas": base64.b64encode(xml_content),
                "mimetype": "application/xml",
                "res_model": self._name,
                "res_id": self.id,
            }
        )
        return {
            "type": "ir.actions.act_url",
            "url": "/web/content/%d?download=true" % attachment.id,
            "target": "self",
        }
