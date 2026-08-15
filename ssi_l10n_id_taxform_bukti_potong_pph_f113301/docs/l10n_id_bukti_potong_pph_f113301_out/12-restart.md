# Restart Bukti Potong PPh f.1.1.33.01 Out

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_f113301`\
> **Model:** `l10n_id.bukti_potong_pph_f113301_out`\
> **Menu:** Taxform > Bukti Potong > PPh 21/26 Tidak Final (f.1.1.33.01) Out\
> **Actor:** user in group `Bukti Potong PPh 21/26 F.1.1.33.01 Out / Validator`\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Config:** The active `policy.template` grants `restart_ok` for that state to the
  actor's group.
- **Access:** User is in group `Bukti Potong PPh 21/26 F.1.1.33.01 Out / Validator`.

## Flow

1. Open the **Taxform > Bukti Potong > PPh 21/26 Tidak Final (f.1.1.33.01) Out** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
