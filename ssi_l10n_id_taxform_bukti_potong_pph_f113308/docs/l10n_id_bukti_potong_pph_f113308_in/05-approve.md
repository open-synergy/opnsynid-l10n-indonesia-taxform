# Approve Bukti Potong PPh f.1.1.33.08 In

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_f113308`\
> **Model:** `l10n_id.bukti_potong_pph_f113308_in`\
> **Menu:** Taxform > Bukti Potong > PPh 26 (f.1.1.33.08) In\
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

1. Open the **Taxform > Bukti Potong > PPh 26 (f.1.1.33.08) In** menu.
2. Open the record to approve.
3. Click **Edit** and confirm the **Number** field is still read-only (not yet
   editable), then discard the edit — proves the number cannot be changed while still
   Waiting for Approval.
4. Click the **Approve** button.
5. Click **OK** on the confirmation dialog.
6. Click **Edit** and confirm the **Number** field is now editable, then discard the
   edit — proves the field only becomes editable once the document reaches On Progress.

## Post-Condition

- If there are still pending approval levels, status remains **Waiting for Approval**
  and the **Number** field remains read-only, the same as in Draft.
- If all approval levels are fulfilled, the document automatically moves to **On
  Progress** status. The document number (Bukti Potong number) is assigned at this point
  if it was left as `/`, and the field becomes editable for entering an official number
  obtained from an external source (e.g. Coretax). Finishing the document afterwards is
  a separate manual step — see `09-done.md`.
