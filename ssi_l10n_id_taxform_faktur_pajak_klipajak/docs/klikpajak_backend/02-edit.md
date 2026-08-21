# Edit Klik Pajak Backend

> **Module:** `ssi_l10n_id_taxform_faktur_pajak_klipajak`\
> **Model:** `klikpajak_backend`\
> **Menu:** Settings > Technical > Klik Pajak > Backends\
> **Actor:** user in group _Settings — Technical Features_ (`base.group_system`)\
> **Requires:** `01-create`

## Pre-Condition

- **Access:** User is in group _Settings — Technical Features_ (`base.group_system`).
- **Access:** Developer mode is active (e.g. open `/web?debug=1`, or enable it via
  **Settings > General Settings > Developer Tools**). The **Technical** menu lives under
  `base.group_no_one`, which stays hidden from the menu bar for any session outside
  developer mode — even for users who already hold the group.

## Flow

1. Open the **Settings > Technical > Klik Pajak > Backends** menu.
2. Find and open the record to edit.
3. Change the required fields: **Name**, **Base URL**, the four API endpoint paths, the
   **Authentication** tab fields, or the **Active** toggle.
4. On the **Parameters** tab, add, edit, or remove rows the same way as during creation
   (see `01-create.md`) — e.g. click an existing row's **Value** cell and type a new
   value.
5. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- If the backend is currently **Running**, the change takes effect immediately for the
  next API call — there is no separate "apply" step.
