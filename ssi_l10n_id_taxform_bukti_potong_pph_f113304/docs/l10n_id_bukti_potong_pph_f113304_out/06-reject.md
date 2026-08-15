# Reject Bukti Potong PPh f.1.1.33.04 Out

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_f113304`\
> **Model:** `l10n_id.bukti_potong_pph_f113304_out`\
> **Menu:** Taxform > Bukti Potong > PPh 22 (f.1.1.33.04) Out\
> **Actor:** approver on the approval level that is currently pending\
> **State:** `confirm` → `reject`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** The active `policy.template` grants `reject_ok` to users registered as the
  active approver.
- **Access:** User is registered as an approver on the approval level that is currently
  pending.

## Flow

1. Open the **Taxform > Bukti Potong > PPh 22 (f.1.1.33.04) Out** menu.
2. Open the record to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**.
