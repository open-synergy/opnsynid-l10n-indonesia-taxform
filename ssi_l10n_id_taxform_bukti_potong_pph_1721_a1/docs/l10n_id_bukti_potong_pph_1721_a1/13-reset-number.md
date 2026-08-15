# Reset Document Number — Tax Form 1721 A1

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_1721_a1`\
> **Model:** `l10n_id.bukti_potong_pph_1721_a1`\
> **Menu:** Taxform > Bukti Potong > Tax Form 1721 A1\
> **Actor:** user in group `Bukti Potong PPh 21 1721 A1 / Validator`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** User is in group `Bukti Potong PPh 21 1721 A1 / Validator`.

## Flow

1. Open the **Taxform > Bukti Potong > Tax Form 1721 A1** menu.
2. Open the record whose document number will be reset.
3. Click the **Reset Document Number** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number when it transitions to the next state,
  according to the sequence template configuration.
