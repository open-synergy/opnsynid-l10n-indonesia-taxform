# Create Bukti Potong PPh f.1.1.33.02 Out

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_f113302_operating_unit`\
> **Extends:** `ssi_l10n_id_taxform_bukti_potong_pph_f113302` — model `l10n_id.bukti_potong_pph_f113302_out`,
> aksi `01-create`

## Additional Fields

When this module is installed, the create form gains one field:

- **Operating Unit**: The operating unit the document belongs to. Only shown to users
  who belong to more than one operating unit (group
  `operating_unit.group_multi_operating_unit`). Defaults to the current user's default
  operating unit. Change if needed.

## Modified — Record Visibility

- The Bukti Potong PPh f.1.1.33.02 Out list is now filtered by operating unit (record
  rule). A user only sees documents belonging to operating units they are assigned to.
  This is not a Flow step.
