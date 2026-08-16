# Cancel Bukti Potong PPh f.1.1.33.10 In

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_f113310`\
> **Model:** `l10n_id.bukti_potong_pph_f113310_in`\
> **Menu:** Taxform > Bukti Potong > PPh 4(2) (f.1.1.33.10) In\
> **Actor:** user in group `Bukti Potong PPh 4(2) (f.1.1.33.10) In / Validator`\
> **State:** `draft` | `confirm` | `done` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, or **Done**.
- **Config:** The active `policy.template` grants `cancel_ok` for that state to the
  actor's group.
- **Access:** User is in group `Bukti Potong PPh 4(2) (f.1.1.33.10) In / Validator`.

## Flow

1. Open the **Taxform > Bukti Potong > PPh 4(2) (f.1.1.33.10) In** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- If the document was **Done**, its accounting entry is unreconciled and removed.
