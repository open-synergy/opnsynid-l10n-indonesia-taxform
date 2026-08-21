# Create Employee

> **Module:** ssi_l10n_id_taxform_pph_21_payslip
>
> **Extends:** ssi_hr_employee — model `hr.employee`, aksi `01-create`

## Additional Post-Condition

- **Joining Tax Period** and **Joining Tax Year** are automatically computed from **Join
  Date** and displayed read-only right after it on the employee form. They identify the
  Indonesian PPh 21 tax period/year the employee's join date falls into, and are
  recomputed whenever **Join Date** changes.
