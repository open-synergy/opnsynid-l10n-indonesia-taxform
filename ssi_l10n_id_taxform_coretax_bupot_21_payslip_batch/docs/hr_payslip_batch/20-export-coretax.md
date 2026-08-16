# Export Coretax PPh 21 XML of Employee Payslip Batch

> **Module:** ssi_l10n_id_taxform_coretax_bupot_21_payslip_batch\
> **Model:** `hr.payslip_batch`\
> **Extends:** ssi_hr_payroll_batch — model `hr.payslip_batch`\
> **Menu:** Human Resource > Payroll > Payslip Batches\
> **Actor:** user in group `Payslip Batch / User`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **Done** (the button is hidden on any other status).
- **Data:** The batch company's partner has _Tax ID (NPWP)_ and _NITKU_ set — used as
  the withholder (`TIN` / `IDPlaceOfBusinessActivity`) in the XML header.
- **Data:** For every employee whose payslip is subject to PPh 21, the employee's
  private address partner has _Tax ID (NPWP/NIK)_ and _PTKP Category_ set.
- **Data:** A PPh 21 TER (Tarif Efektif Rata-Rata) table is configured for the batch's
  period — used to look up the withholding rate.
- **Access:** User is in group `Payslip Batch / User` (required to open and act on the
  batch where this button appears; the button itself is not guarded by a dedicated
  policy field).

## Flow

1. Open the **Human Resource > Payroll > Payslip Batches** menu.
2. Open the batch to export (status **Done**).
3. On the **Payslips** tab, click the **Export Coretax PPh 21 XML** button.
4. In the wizard that appears, select the **Gross Income Salary Rule** (the rule that
   holds each payslip's gross income) and the **Withheld PPh 21 Salary Rule** (the rule
   that holds each payslip's withheld PPh 21 amount).
5. Click **Export**.

## Post-Condition

- On success, the wizard closes and the browser downloads an XML file named
  `coretax_bupot_21_<number>.xml` (or `coretax_bupot_21_<database id>.xml` when the
  batch has no document number yet). It follows the Coretax bulk import schema
  (`MmPayrollBulk`) and contains one entry per payslip whose amount on the selected
  Withheld PPh 21 Salary Rule is greater than zero; payslips with no withheld PPh 21 are
  left out.
- The batch and its payslips are not modified; the batch's status is unchanged.
- If the withholder company partner is missing its Tax ID or NITKU, if a taxed
  employee's private address partner is missing its Tax ID or PTKP Category, or if no
  payslip in the batch has PPh 21 withheld, Export fails as a whole with an error
  message and the wizard stays open — no file is downloaded.
