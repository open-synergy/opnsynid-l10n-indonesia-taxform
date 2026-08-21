# Create Faktur Pajak Keluaran

> **Module:** `ssi_l10n_id_taxform_faktur_pajak_operating_unit`\
> **Extends:** `ssi_l10n_id_taxform_faktur_pajak` — model `faktur_pajak_keluaran`, aksi `01-create`

## Additional Fields

When this module is installed, the create form gains one additional field:

- **Operating Unit**: The operating unit that owns this record. Only visible when the
  user belongs to the `Multi Operating Unit` group. Defaults to the current user's
  default operating unit; change if needed. Not required — the document can still be
  created without one.

## Additional Post-Condition

- When **Operating Unit** is set, the e-Faktur **Seller ID TKU** field is recomputed
  from the operating unit's partner `nitku` instead of the company's own data.
- When **Operating Unit** is set, the e-Faktur **Company NPWP** field is recomputed from
  the operating unit's partner `vat` instead of the company's own partner `vat`. Both
  fields remain informational (read-only, computed) and are used when exporting the
  e-Faktur/Core Tax report.

## Modified — Record Visibility

- The list is now filtered by operating unit (record rule). A user in the
  `Operating Unit` data-ownership group only sees records whose Operating Unit is among
  the operating units assigned to them. This is not a Flow step.
