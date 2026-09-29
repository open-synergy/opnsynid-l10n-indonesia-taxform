# Done Bukti Potong PPh f.1.1.33.10 Out

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_f113310`\
> **Model:** `l10n_id.bukti_potong_pph_f113310_out`\
> **Menu:** Taxform > Bukti Potong > PPh 4(2) (f.1.1.33.10) Out\
> **Actor:** user in group `Bukti Potong PPh 4(2) (f.1.1.33.10) Out / User`\
> **State:** `open` → `done`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Config:** The active `policy.template` for this model grants `done_ok` for state
  `open` to the actor's group.
- **Access:** User is in group `Bukti Potong PPh 4(2) (f.1.1.33.10) Out / User`.

## Flow

1. Open the **Taxform > Bukti Potong > PPh 4(2) (f.1.1.33.10) Out** menu.
2. Open the record to finish.
3. If the document number (`# Document` field) is still `/`, or needs to be replaced
   with an official number obtained externally (e.g. from Coretax), edit it now — it is
   still editable while status is **On Progress**.
4. Click the **Done** button.
5. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
- The document number is no longer editable.
- The related accounting entry (**Accounting** tab) is generated and posted.
