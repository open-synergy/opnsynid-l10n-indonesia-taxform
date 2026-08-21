# Create Taxform Objek Pajak

> **Module:** ssi_l10n_id_taxform
>
> **Model:** `l10n_id.taxform_objek_pajak`
>
> **Menu:** Taxform > Configuration > Objek Pajak
>
> **Actor:** user in group _Objek Pajak_

## Pre-Condition

- **Access:** User is in group _Objek Pajak_.

## Flow

1. Open the **Taxform > Configuration > Objek Pajak** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Kode Objek Pajak** _(required)_: Enter a unique code, or enter **/** to leave it
     eligible for automatic assignment.
   - **Description** _(required)_: Enter a description of the tax object.
4. Optionally fill in **Note**.
5. Click **Save**.

## Post-Condition

- A new tax object record is created, active by default.
- **Company** is not shown on the form; it is filled automatically with the current
  user's company (`_default_company_id`) and cannot be changed from this screen.
