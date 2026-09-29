# Input Coretax Number on Bukti Potong PPh f.1.1.33.01 Out

> **Module:** `ssi_l10n_id_taxform_coretax_bupot_pph_f113301`\
> **Model:** `l10n_id.bukti_potong_pph_f113301_out`\
> **Menu:** Taxform > Bukti Potong > PPh 21/26 Tidak Final (f.1.1.33.01) Out\
> **Actor:** user in group `Bukti Potong PPh 21/26 F.1.1.33.01 Out / User`\
> **State:** `open` (no transition)\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress** (`open`), reached once approval is fully
  completed via `05-approve`.
- **Record:** The document has been uploaded to Coretax outside Odoo and DGT has replied
  with the official Bukti Potong number.
- **Access:** User is in group `Bukti Potong PPh 21/26 F.1.1.33.01 Out / User`.

## Flow

1. Open the **Taxform > Bukti Potong > PPh 21/26 Tidak Final (f.1.1.33.01) Out** menu.
2. Find and open the record that is **On Progress**.
3. Click **Edit**.
4. Type the official Coretax number into the **Number** field (shown next to the status
   bar), replacing the default `/`.
5. Click **Save**.

## Post-Condition

- The record's **Number** shows the Coretax number that was typed in.
- The number is kept unchanged through **Done** (`09-done`) — the internal sequence
  never runs for this document (`_create_sequence_state = False`), so nothing overwrites
  the manually-typed number.
