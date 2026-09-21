# Input Coretax Number on Bukti Potong PPh f.1.1.33.01 Out

> **Module:** `ssi_l10n_id_taxform_coretax_bupot_pph_f113301`\
> **Model:** `l10n_id.bukti_potong_pph_f113301_out`\
> **Menu:** Taxform > Bukti Potong > PPh 21/26 Tidak Final (f.1.1.33.01) Out\
> **Actor:** user in group `Bukti Potong PPh 21/26 F.1.1.33.01 Out / User`\
> **State:** `confirm` (no transition)\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval** (`confirm`), reached via `04-confirm`.
- **Record:** The document has been uploaded to Coretax outside Odoo and DGT has replied
  with the official Bukti Potong number.
- **Access:** User is in group `Bukti Potong PPh 21/26 F.1.1.33.01 Out / User`.

## Flow

1. Open the **Taxform > Bukti Potong > PPh 21/26 Tidak Final (f.1.1.33.01) Out** menu.
2. Find and open the record that is **Waiting for Approval**.
3. Click **Edit**.
4. Type the official Coretax number into the **Number** field (shown next to the status
   bar), replacing the default `/`.
5. Click **Save**.

## Post-Condition

- The record's **Number** shows the Coretax number that was typed in.
- The number is kept unchanged through **Approve** (`05-approve`) — the internal
  sequence no longer overwrites it when the document reaches **Done**.
