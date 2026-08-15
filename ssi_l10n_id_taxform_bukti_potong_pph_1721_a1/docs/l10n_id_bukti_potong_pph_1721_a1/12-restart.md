# Restart Tax Form 1721 A1

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_1721_a1`\
> **Model:** `l10n_id.bukti_potong_pph_1721_a1`\
> **Menu:** Taxform > Bukti Potong > Tax Form 1721 A1\
> **Actor:** user in group `Bukti Potong PPh 21 1721 A1 / Validator`\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Config:** The active `policy.template` grants `restart_ok` for that state to the
  actor's group.
- **Access:** User is in group `Bukti Potong PPh 21 1721 A1 / Validator`.

## Flow

1. Open the **Taxform > Bukti Potong > Tax Form 1721 A1** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- All approval records are removed and the approval template is cleared. A later Confirm
  starts the approval process from the beginning.
