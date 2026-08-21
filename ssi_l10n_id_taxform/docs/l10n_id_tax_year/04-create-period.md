# Create Period for Tax Year

> **Module:** ssi_l10n_id_taxform
>
> **Model:** `l10n_id.tax_year`
>
> **Menu:** Taxform > Configuration > Tax Periods > Tax Years
>
> **Actor:** user in group _Tax Year_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The tax year record exists, with **Date Start** and **Date End** set.
- **Access:** User is in group _Tax Year_.

## Flow

1. Open the **Taxform > Configuration > Tax Periods > Tax Years** menu.
2. Open the tax year record to generate periods for.
3. In the header, click **Create Period**.

## Post-Condition

- One **l10n_id.tax_period** record is created for each calendar month between the tax
  year's **Date Start** and **Date End**. For a tax year spanning 01/01/2024 to
  12/31/2024, this creates **12** period records (01/2024 through 12/2024).
- Each generated period's **Tax Period** and **Code** are set to the month/year in
  `MM/YYYY` format (for example "01/2024"), its **Date Start** is the first day of that
  calendar month, and its **Date End** is the last day of that calendar month — clamped
  to the tax year's own **Date End** for the last period if the tax year does not end
  exactly on a month boundary.
- The new periods appear in the **Periods** tab of the tax year record.
- Clicking **Create Period** again on the same tax year appends another full set of
  periods; existing periods are not checked for duplicates or replaced.
