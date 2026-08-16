# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError

# Coretax tax object code for permanent employee monthly withholding
# (Bukti Pemotongan Masa Pegawai - formulir 1721-VIII).
CORETAX_TAX_OBJECT_CODE = "21-100-01"
# Citizenship status of the income recipient. Permanent employees handled by
# this export are domestic taxpayers.
CORETAX_COUNTERPART_OPT = "Resident"
# Tax facility. "N/A" means no facility is used.
CORETAX_TAX_CERTIFICATE = "N/A"


class HrPayslipBatch(models.Model):
    """Add Coretax PPh 21 BPMP XML export helpers to the payslip batch.

    Builds the rendering context consumed by the Coretax BPMP XML report
    (``report.ssi_l10n_id_taxform_coretax_bupot_21_payslip_batch.bpmp``):
    the withholder header plus one slip per payslip whose withheld PPh 21
    is greater than zero.
    """

    _inherit = "hr.payslip_batch"

    def _coretax_format_number(self, value):
        """Render a numeric value without a trailing ``.0`` so that integer
        amounts and rates are written as plain integers in the XML."""
        if value == int(value):
            return str(int(value))
        return repr(float(value))

    def _get_coretax_pemotong(self):
        """Return the withholder identity for the Coretax header: the NPWP
        (``TIN``) and the 22-character ID TKU (``IDPlaceOfBusinessActivity``).

        Both are taken from the batch company partner: ``vat`` for the NPWP and
        ``nitku`` for the ID TKU."""
        self.ensure_one()
        company = self.company_id or self.env.company
        partner = company.partner_id
        tin = (partner.vat or "").strip()
        id_tku = (partner.nitku or "").strip()
        if not tin or not id_tku:
            error_message = _(
                """
Context: Generate Coretax PPh 21 withholding XML
Database ID: %s
Problem: The withholder company "%s" has no %s configured
Solution: Set the NPWP (Tax ID) and NITKU of the company partner
"""
                % (
                    self.id,
                    company.display_name,
                    not tin and "NPWP (Tax ID)" or "NITKU (ID TKU)",
                )
            )
            raise UserError(error_message)
        return tin, id_tku

    def _get_coretax_slip_value(self, payslip, rule):
        """Sum the total of the payslip lines that use ``rule``."""
        lines = payslip.line_ids.filtered(lambda line: line.rule_id == rule)
        return sum(lines.mapped("total"))

    def _prepare_coretax_slip(self, payslip, bruto_rule, pph_rule):
        """Build the dictionary describing one ``MmPayroll`` element, or return
        ``False`` when the payslip is not subject to PPh 21 (withheld tax is not
        greater than zero)."""
        self.ensure_one()
        pph = self._get_coretax_slip_value(payslip, pph_rule)
        if pph <= 0.0:
            return False

        gross = self._get_coretax_slip_value(payslip, bruto_rule)
        employee = payslip.employee_id
        partner = employee.address_home_id
        tin = (partner.vat or "").strip()
        ptkp_category = partner.ptkp_category_id

        problems = []
        if not tin:
            problems.append("NPWP/NIK (Tax ID) of the employee's private address")
        if not ptkp_category:
            problems.append("PTKP Category of the employee's private address")
        if problems:
            error_message = _(
                """
Context: Generate Coretax PPh 21 withholding XML
Database ID: %s
Problem: Employee "%s" is missing: %s
Solution: Complete the data above before generating the XML
"""
                % (self.id, employee.display_name, ", ".join(problems))
            )
            raise UserError(error_message)

        ter = self.env["l10n_id.pph_21_ter"].find(payslip.date)
        rate = ter.compute_tax(gross, [ptkp_category.id])["rate"]

        return {
            "tax_period_month": payslip.date.month,
            "tax_period_year": payslip.date.year,
            "counterpart_opt": CORETAX_COUNTERPART_OPT,
            "counterpart_tin": tin,
            "status_tax_exemption": ptkp_category.code,
            "position": employee.job_id.name or "",
            "tax_certificate": CORETAX_TAX_CERTIFICATE,
            "tax_object_code": CORETAX_TAX_OBJECT_CODE,
            "gross": self._coretax_format_number(gross),
            "rate": self._coretax_format_number(rate),
            "withholding_date": fields.Date.to_string(payslip.date),
        }

    def _prepare_coretax_bupot_21_values(self, bruto_rule, pph_rule):
        """Build the full rendering context for the Coretax BPMP XML report:
        the withholder header plus one slip per payslip that is subject to
        PPh 21. Raises a ``UserError`` when any required data is missing."""
        self.ensure_one()
        tin, id_tku = self._get_coretax_pemotong()

        slips = []
        for payslip in self.payslip_ids:
            slip = self._prepare_coretax_slip(payslip, bruto_rule, pph_rule)
            if slip:
                slip["id_place_of_business_activity"] = id_tku
                slips.append(slip)

        if not slips:
            error_message = _(
                """
Context: Generate Coretax PPh 21 withholding XML
Database ID: %s
Problem: No payslip in this batch has PPh 21 withheld (greater than zero)
Solution: Select a salary rule that holds the withheld PPh 21 amount
"""
                % (self.id)
            )
            raise UserError(error_message)

        return {
            "company_tin": tin,
            "company_id_tku": id_tku,
            "slips": slips,
        }
