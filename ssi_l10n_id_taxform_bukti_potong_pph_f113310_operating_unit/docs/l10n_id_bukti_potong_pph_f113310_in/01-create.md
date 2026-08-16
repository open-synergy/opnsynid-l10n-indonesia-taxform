# Create Bukti Potong PPh f.1.1.33.10 In

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_f113310_operating_unit`\
> **Extends:** `ssi_l10n_id_taxform_bukti_potong_pph_f113310` — model `l10n_id.bukti_potong_pph_f113310_in`,
> aksi `01-create`

## Additional Fields

When this module is installed, the create form gains one additional field:

- **Operating Unit**: The operating unit that owns this record. Only visible when the
  user belongs to the `Multi Operating Unit` group. Defaults to the current user's
  default operating unit; change if needed.

## Modified — Record Visibility

- The list is now filtered by operating unit (record rule). A user in the
  `Operating Unit` data-ownership group only sees records whose Operating Unit is among
  the operating units assigned to them. This is not a Flow step.
