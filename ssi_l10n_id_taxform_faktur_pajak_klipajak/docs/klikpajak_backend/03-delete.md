# Delete Klik Pajak Backend

> **Module:** `ssi_l10n_id_taxform_faktur_pajak_klipajak`\
> **Model:** `klikpajak_backend`\
> **Menu:** Settings > Technical > Klik Pajak > Backends\
> **Actor:** user in group _Settings — Technical Features_ (`base.group_system`)\
> **Requires:** `01-create`

## Pre-Condition

- **Access:** User is in group _Settings — Technical Features_ (`base.group_system`),
  the only group granted delete rights on this model.
- **Access:** Developer mode is active (e.g. open `/web?debug=1`, or enable it via
  **Settings > General Settings > Developer Tools**). The **Technical** menu lives under
  `base.group_no_one`, which stays hidden from the menu bar for any session outside
  developer mode — even for users who already hold the group.

## Flow

1. Open the **Settings > Technical > Klik Pajak > Backends** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records, together with their parameter rows, are permanently removed from
  the system.
- If a deleted record was the company's active running backend, the company's **Active
  Klikpajak Backend** reference is cleared automatically.
