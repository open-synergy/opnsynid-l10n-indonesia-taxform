# Create Tax Period

> **Module:** ssi_l10n_id_taxform
>
> **Model:** `l10n_id.tax_period`
>
> **Menu:** Taxform > Configuration > Tax Periods > Tax Periods
>
> **Actor:** user in group _Tax Period_
>
> **Requires:** `ssi_l10n_id_taxform/l10n_id_tax_year/01-create`

## Pre-Condition

- **Data:** An **l10n_id.tax_year** record exists to link this period to (see
  `ssi_l10n_id_taxform/l10n_id_tax_year/01-create`). Periods are normally generated
  automatically from a tax year's **Create Period** button
  (`ssi_l10n_id_taxform/l10n_id_tax_year/04-create-period`) rather than created manually
  here.
- **Access:** User is in group _Tax Period_.

## Flow

1. Open the **Taxform > Configuration > Tax Periods > Tax Periods** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Tax Period** _(required)_: Enter a label for the period (for example "01/2024").
   - **Code** _(required)_: Enter a unique code, or enter **/** to leave it eligible for
     automatic assignment.
   - **Tax Year**: Select the tax year this period belongs to. Not required to save this
     record, but a period without a **Tax Year** is not reachable from any tax year's
     **Periods** tab.
   - **Date Start** _(required)_: The first day covered by this period (for example
     01/01/2024).
   - **Date End** _(required)_: The last day covered by this period (for example
     01/31/2024). Must not be earlier than **Date Start**.
4. Optionally fill in **Note**.
5. Click **Save**.

## Post-Condition

- A new tax period record is created, active by default.
