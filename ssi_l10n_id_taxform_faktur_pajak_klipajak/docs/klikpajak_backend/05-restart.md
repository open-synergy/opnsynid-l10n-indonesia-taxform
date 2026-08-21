# Restart Klik Pajak Backend

> **Module:** `ssi_l10n_id_taxform_faktur_pajak_klipajak`\
> **Model:** `klikpajak_backend`\
> **Menu:** Settings > Technical > Klik Pajak > Backends\
> **Actor:** user in group _Settings — Technical Features_ (`base.group_system`)\
> **State:** `running` → `draft`\
> **Requires:** `04-running`

## Pre-Condition

- **Record:** Status is **Running**.
- **Access:** User is in group _Settings — Technical Features_ (`base.group_system`).
- **Access:** Developer mode is active (e.g. open `/web?debug=1`, or enable it via
  **Settings > General Settings > Developer Tools**). The **Technical** menu lives under
  `base.group_no_one`, which stays hidden from the menu bar for any session outside
  developer mode — even for users who already hold the group.

## Flow

1. Open the **Settings > Technical > Klik Pajak > Backends** menu.
2. Find and open the record to restart.
3. Click the **Restart** button in the header.

## Post-Condition

- The record's status changes back to **Draft**.
- The company's **Active Klikpajak Backend** reference
  (`res.company.klikpajak_backend_id`) is cleared.
