# Confirm Tax Form 1721 A1

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_1721_a1`\
> **Model:** `l10n_id.bukti_potong_pph_1721_a1`\
> **Menu:** Taxform > Bukti Potong > Tax Form 1721 A1\
> **Actor:** user in group `Bukti Potong PPh 21 1721 A1 / User`\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** The active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level.
- **Access:** User is in group `Bukti Potong PPh 21 1721 A1 / User`.

## Flow

1. Open the **Taxform > Bukti Potong > Tax Form 1721 A1** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for each approver level defined by the approval template.
