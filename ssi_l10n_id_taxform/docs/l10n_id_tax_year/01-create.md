# Create Tax Year

> **Module:** ssi_l10n_id_taxform
>
> **Model:** `l10n_id.tax_year`
>
> **Menu:** Taxform > Configuration > Tax Periods > Tax Years
>
> **Actor:** user in group _Tax Year_

## Pre-Condition

- **Access:** User is in group _Tax Year_.

## Flow

1. Open the **Taxform > Configuration > Tax Periods > Tax Years** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Tax Year** _(required)_: Enter a label for the tax year (for example "2024").
   - **Code** _(required)_: Enter a unique code, or enter **/** to leave it eligible for
     automatic assignment.
   - **Date Start** _(required)_: The first day covered by this tax year (for example
     01/01/2024).
   - **Date End** _(required)_: The last day covered by this tax year (for example
     12/31/2024). Must not be earlier than **Date Start**.
4. Optionally fill in **Note**.
5. Click **Save**.

## Post-Condition

- A new tax year record is created, active by default, with an empty **Periods** list.
