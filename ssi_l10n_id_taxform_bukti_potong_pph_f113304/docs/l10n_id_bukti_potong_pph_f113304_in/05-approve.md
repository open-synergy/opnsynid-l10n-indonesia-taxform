# Approve Bukti Potong PPh f.1.1.33.04 In

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_f113304`\
> **Model:** `l10n_id.bukti_potong_pph_f113304_in`\
> **Menu:** Taxform > Bukti Potong > PPh 22 (f.1.1.33.04) In\
> **Actor:** approver on the approval level that is currently pending\
> **State:** `confirm` → `confirm` | `open`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** The active `policy.template` grants `approve_ok` to users registered as
  the active approver.
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. When the template uses sequential approval, only the first unapproved
  level is pending.

## Flow

1. Open the **Taxform > Bukti Potong > PPh 22 (f.1.1.33.04) In** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.
- If all approval levels are fulfilled, the document automatically moves to **On
  Progress** status. The document number (Bukti Potong number) is assigned at this point
  if it was left as `/`, and the field becomes editable for entering an official number
  obtained from an external source (e.g. Coretax). Finishing the document afterwards is
  a separate manual step — see `09-done.md`.
