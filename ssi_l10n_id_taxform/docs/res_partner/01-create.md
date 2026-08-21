# Create Contact

> **Module:** ssi_l10n_id_taxform\
> **Extends:** res.partner (Odoo core Contacts) — no base Instruksi Kerja exists for this
> model

## Additional Fields

When this module is installed, the Contacts form gains one field, placed right after
**Tax ID**:

- **NITKU**: Nomor Induk Tempat Kegiatan Usaha — the taxpayer's place-of-business
  registration number used for Indonesian tax reporting. Optional free-text field. Shown
  on the main contact form for every contact, and also on the inline **Contact &amp;
  Address** row form, where it is only visible when that row's **Address Type** is set
  to **Branch Address** (a value only selectable when the `ssi_partner` module, which
  adds it, is also installed).
