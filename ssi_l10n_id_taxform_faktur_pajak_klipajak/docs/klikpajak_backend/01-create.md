# Create Klik Pajak Backend

> **Module:** `ssi_l10n_id_taxform_faktur_pajak_klipajak`\
> **Model:** `klikpajak_backend`\
> **Menu:** Settings > Technical > Klik Pajak > Backends\
> **Actor:** user in group _Settings — Technical Features_ (`base.group_system`)\
> **State:** `—` → `draft`

## Pre-Condition

- **Access:** User is in group _Settings — Technical Features_ (`base.group_system`),
  the only group granted create rights on this model.

## Flow

1. Open the **Settings > Technical > Klik Pajak > Backends** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** and **Code**: leave **Code** as **/** unless a specific identifier is
     needed.
   - **Company**: only shown in multi-company databases; defaults to the current user's
     company.
   - **Base URL**: the Klikpajak API base URL.
   - **Create Sale Invoice**, **Retrieve Sale Invoice**, **Approve Sale Invoice**,
     **Cancel Sale Invoice**: the four API endpoint paths, pre-filled with the standard
     Klikpajak paths. Adjust only if the provider requires different paths.
4. On the **Authentication** tab, select **Authentication** (JWT, Basic Authentication,
   or HMAC — HMAC is selected by default) and fill in the matching credential fields:
   - **JWT**: **Token**.
   - **Basic Authentication**: **Username** and **Password**.
   - **HMAC**: **Client ID** and **Client Secret**.
5. On the **Parameters** tab, add a row for each extra API parameter needed: fill in
   **Parameter Name**, **Parameter Type**, and **Value** directly in the table, or click
   a row to open its detail form and also fill in **Description**. This step is optional
   — a backend can be created without any parameter rows.
6. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- The record is **not** yet linked to the company's active Klikpajak backend — that only
  happens after **Running** is clicked (see `04-running.md`).
