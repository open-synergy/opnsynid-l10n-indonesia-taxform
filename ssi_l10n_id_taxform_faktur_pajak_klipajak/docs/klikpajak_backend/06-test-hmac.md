# Test HMAC Signature of a Klik Pajak Backend

> **Module:** `ssi_l10n_id_taxform_faktur_pajak_klipajak`\
> **Model:** `klikpajak_backend`\
> **Menu:** Settings > Technical > Klik Pajak > Backends\
> **Actor:** user in group _Settings — Technical Features_ (`base.group_system`)\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** **Authentication** is set to **HMAC**, with **Client ID** and **Client
  Secret** filled in — the button only computes a signature for the HMAC method.
- **Access:** User is in group _Settings — Technical Features_ (`base.group_system`).
- **Access:** Developer mode is active (e.g. open `/web?debug=1`, or enable it via
  **Settings > General Settings > Developer Tools**). The **Technical** menu lives under
  `base.group_no_one`, which stays hidden from the menu bar for any session outside
  developer mode — even for users who already hold the group.

## Flow

1. Open the **Settings > Technical > Klik Pajak > Backends** menu.
2. Find and open the record to test.
3. Click the **Test HMAC** button in the header.

## Post-Condition

- A dialog appears showing the computed signature as **"Result: `<signature>`"**. This
  dialog **is** the expected outcome of clicking **Test HMAC** — it is how the value is
  surfaced to the user, not an error condition.
- The record itself is unchanged: no field value or status is modified by this action,
  and no request is sent to the Klikpajak API.
