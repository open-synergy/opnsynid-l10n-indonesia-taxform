# Restart Approval Process — Bukti Potong PPh f.1.1.33.06 In

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_f113306`\
> **Model:** `l10n_id.bukti_potong_pph_f113306_in`\
> **Menu:** Taxform > Bukti Potong > PPh 23 (f.1.1.33.06) In\
> **Actor:** user in group `Bukti Potong PPh 23 (f.1.1.33.06) In / Validator`\
> **State:** `confirm` → `confirm`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** The active `policy.template` grants `restart_approval_ok` for state
  `confirm` to the actor's group.
- **Access:** User is in group `Bukti Potong PPh 23 (f.1.1.33.06) In / Validator`.

## Flow

1. Open the **Taxform > Bukti Potong > PPh 23 (f.1.1.33.06) In** menu.
2. Open the record whose approval process needs to be restarted.
3. Click the **Restart Approval Process** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status remains **Waiting for Approval**.
- The approval records for this document are recreated from the approval template,
  restarting the approval sequence from the first level.
