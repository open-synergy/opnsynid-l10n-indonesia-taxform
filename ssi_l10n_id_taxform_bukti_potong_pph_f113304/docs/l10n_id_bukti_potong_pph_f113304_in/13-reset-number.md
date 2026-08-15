# Reset Document Number — Bukti Potong PPh f.1.1.33.04 In

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_f113304`\
> **Model:** `l10n_id.bukti_potong_pph_f113304_in`\
> **Menu:** Taxform > Bukti Potong > PPh 22 (f.1.1.33.04) In\
> **Actor:** user in group `Bukti Potong PPh 22 (f.1.1.33.04) In / Validator`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** User is in group `Bukti Potong PPh 22 (f.1.1.33.04) In / Validator`.

## Flow

1. Open the **Taxform > Bukti Potong > PPh 22 (f.1.1.33.04) In** menu.
2. Open the record whose document number will be reset.
3. Click the **Reset Document Number** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number when it transitions to the next state,
  according to the sequence template configuration.
