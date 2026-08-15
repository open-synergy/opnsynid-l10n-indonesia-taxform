# Cancel Tax Form 1721 A1

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_1721_a1`\
> **Model:** `l10n_id.bukti_potong_pph_1721_a1`\
> **Menu:** Taxform > Bukti Potong > Tax Form 1721 A1\
> **Actor:** user in group `Bukti Potong PPh 21 1721 A1 / Validator`\
> **State:** `draft` | `confirm` | `done` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, or **Done**.
- **Config:** The active `policy.template` grants `cancel_ok` for that state to the
  actor's group.
- **Access:** User is in group `Bukti Potong PPh 21 1721 A1 / Validator`.

## Flow

1. Open the **Taxform > Bukti Potong > Tax Form 1721 A1** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
