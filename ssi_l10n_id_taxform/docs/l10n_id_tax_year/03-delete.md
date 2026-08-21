# Delete Tax Year

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

- **Access:** User is in group _Tax Year_.

## Flow

1. Open the **Taxform > Configuration > Tax Periods > Tax Years** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system, together with any
  **l10n_id.tax_period** records still linked to them (the link is configured
  `ondelete="cascade"`).
