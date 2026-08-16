# Create Bukti Potong PPh f.1.1.33.08 In

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_f113308`\
> **Model:** `l10n_id.bukti_potong_pph_f113308_in`\
> **Menu:** Taxform > Bukti Potong > PPh 26 (f.1.1.33.08) In\
> **Actor:** user in group `Bukti Potong PPh 26 (f.1.1.33.08) In / User`\
> **State:** `—` → `draft`

## Pre-Condition

- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group (needed before the record can later be confirmed).
- **Config:** An active `approval.template` for this model exists (needed for the later
  Confirm/Approve flow).
- **Data:** The **Tax Period** master data already exists.
- **Data:** The accounting **Journal** and PPh receivable **Account** already exist.
- **Data:** The **KPP** (tax office, `res.partner`, a company) already exists.
- **Data:** The **Pemotong Pajak** (withholding party, `res.partner`) already exists.
- **Access:** User is in group `Bukti Potong PPh 26 (f.1.1.33.08) In / User`.

## Flow

1. Open the **Taxform > Bukti Potong > PPh 26 (f.1.1.33.08) In** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Company** _(required)_: Automatically filled from the current user's company.
     Change if needed.
   - **Date** _(required)_: Automatically filled with today's date. Change if needed.
   - **Tax Period** _(required)_: Select the applicable tax period.
   - **Journal** _(required)_: Select the accounting journal.
   - **Account** _(required)_: Select the PPh receivable account.
   - **KPP** _(required)_: Select the tax office (KPP) partner.
   - **Wajib Pajak**: Automatically filled from the current company's partner
     (read-only, since this document's Type is "In").
   - **Pemotong Pajak** _(required)_: Select the party that withheld this tax.
   - **TTD**: Optionally select the signer, a contact of the Pemotong Pajak.
4. Optionally, on the **Details** tab, add one or more withholding lines: select the
   **Tax**, fill in the **Amount**, and pick the source **Income Move Lines**. Each
   line's **Tax Amount** is computed automatically.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status. **(14.0: Save keeps the form open in
  read-only mode; it does not navigate back to the list.)**
- The document number stays **/** until the record is confirmed and approved (done).
