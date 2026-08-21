# Run Klik Pajak Backend

> **Module:** `ssi_l10n_id_taxform_faktur_pajak_klipajak`\
> **Model:** `klikpajak_backend`\
> **Menu:** Settings > Technical > Klik Pajak > Backends\
> **Actor:** user in group _Settings — Technical Features_ (`base.group_system`)\
> **State:** `draft` → `running`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Settings — Technical Features_ (`base.group_system`).
- **Access:** Developer mode is active (e.g. open `/web?debug=1`, or enable it via
  **Settings > General Settings > Developer Tools**). The **Technical** menu lives under
  `base.group_no_one`, which stays hidden from the menu bar for any session outside
  developer mode — even for users who already hold the group.

## Flow

1. Open the **Settings > Technical > Klik Pajak > Backends** menu.
2. Find and open the record to run.
3. Click the **Running** button in the header.

## Post-Condition

- The record's status changes to **Running**.
- The record becomes the company's **Active Klikpajak Backend**
  (`res.company.klikpajak_backend_id`).
- **Side effect:** any other backend belonging to the same company that was previously
  **Running** is automatically set back to **Draft** — only one backend per company can
  be **Running** at a time.
