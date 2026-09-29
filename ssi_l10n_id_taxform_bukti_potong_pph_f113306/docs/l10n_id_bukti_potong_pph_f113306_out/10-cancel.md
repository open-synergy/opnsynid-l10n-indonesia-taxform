# Cancel Bukti Potong PPh f.1.1.33.06 Out

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_f113306`\
> **Model:** `l10n_id.bukti_potong_pph_f113306_out`\
> **Menu:** Taxform > Bukti Potong > PPh 23 (f.1.1.33.06) Out\
> **Actor:** user in group `Bukti Potong PPh 23 (f.1.1.33.06) Out / Validator`\
> **State:** `draft` → `confirm` → `open` → `done` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, with all required fields filled in and at least one
  withholding line so the document can reach **Done**.
- **Config:** The active `policy.template` grants `confirm_ok`, `approve_ok`, and
  `done_ok` to the acting user, and grants `cancel_ok` for state **Done** to the actor's
  group.
- **Access:** User is in group `Bukti Potong PPh 23 (f.1.1.33.06) Out / Validator`.

## Flow

1. Open the **Taxform > Bukti Potong > PPh 23 (f.1.1.33.06) Out** menu.
2. Open the record to cancel.
3. Click the **Confirm** button, then click **OK** on the confirmation dialog.
4. Confirm the **Cancel** button is not available while status is **Waiting for
   Approval** — the document must reach **Done** first.
5. Click the **Approve** button, then click **OK** on the confirmation dialog.
6. Click the **Done** button, then click **OK** on the confirmation dialog.
7. Click the **Cancel** button.
8. In the wizard that appears, select the **Cancellation Reason**.
9. Click **Confirm**.
10. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- If the document was **Done**, its accounting entry is unreconciled and removed.
