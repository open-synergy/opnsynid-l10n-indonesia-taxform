# Approve Bukti Potong PPh f.1.1.33.08 Out

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_f113308`\
> **Model:** `l10n_id.bukti_potong_pph_f113308_out`\
> **Menu:** Taxform > Bukti Potong > PPh 26 (f.1.1.33.08) Out\
> **Actor:** approver on the approval level that is currently pending\
> **State:** `confirm` → `confirm` | `done`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** The active `policy.template` grants `approve_ok` to users registered as
  the active approver.
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. When the template uses sequential approval, only the first unapproved
  level is pending.

## Flow

1. Open the **Taxform > Bukti Potong > PPh 26 (f.1.1.33.08) Out** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.
- If all approval levels are fulfilled, the document is automatically finished and
  status changes to **Done** — there is no separate **Done** button; the transition is
  triggered automatically by the last approval, and the related accounting entry
  (**Accounting** tab) is generated and posted.
