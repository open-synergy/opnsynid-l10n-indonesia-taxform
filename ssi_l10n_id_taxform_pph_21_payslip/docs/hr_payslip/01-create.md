# Create Employee Payslip

> **Module:** ssi_l10n_id_taxform_pph_21_payslip
>
> **Extends:** ssi_hr_payroll — model `hr.payslip`, aksi `01-create`

## Additional Post-Condition

- **Payslip Tax Year** and **Payslip Tax Period** are automatically computed from the
  selected **Employee** and **Date**, and displayed read-only right after **Journal** on
  the payslip form.
- **Joining Tax Month** is also computed and displayed there. It shows the month number
  the employee joined in **only when** the payslip's **Payslip Tax Year** matches the
  employee's Joining Tax Year (see `docs/hr_employee/01-create.md` in this module);
  otherwise it defaults to `1`.
