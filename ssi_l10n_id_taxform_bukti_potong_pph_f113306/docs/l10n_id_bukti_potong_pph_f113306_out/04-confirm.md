# Confirm Bukti Potong PPh f.1.1.33.06 Out

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_f113306`\
> **Model:** `l10n_id.bukti_potong_pph_f113306_out`\
> **Menu:** Taxform > Bukti Potong > PPh 23 (f.1.1.33.06) Out\
> **Actor:** user in group `Bukti Potong PPh 23 (f.1.1.33.06) Out / User`\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** The active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level.
- **Access:** User is in group `Bukti Potong PPh 23 (f.1.1.33.06) Out / User`.

## Flow

1. Open the **Taxform > Bukti Potong > PPh 23 (f.1.1.33.06) Out** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for each approver level defined by the approval template.
