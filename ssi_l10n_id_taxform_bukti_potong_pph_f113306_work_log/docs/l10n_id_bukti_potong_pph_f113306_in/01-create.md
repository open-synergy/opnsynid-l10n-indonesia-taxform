# Create Bukti Potong PPh f.1.1.33.06 In

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_f113306_work_log`\
> **Extends:** `ssi_l10n_id_taxform_bukti_potong_pph_f113306` — model `l10n_id.bukti_potong_pph_f113306_in`,
> aksi `01-create`

## Modified Flow

- Anchor: on Flow base step 2 (Click the **New** button. **(14.0: "Create")**). This
  module adds a **Work Log** page to the form (inserted after the last existing tab),
  showing **Estimation**, **Total**, **Remaining**, and **Excess** hour fields, the
  **Work Log Analytic Account** field, and the list of work log entries (`hr.work_log`)
  linked to this document. The page is already rendered on the unsaved create form — no
  field needs to be filled and no state condition applies.
- The page is not gated by document status — it can be opened and filled in any state
  (**Draft**, **Waiting for Approval**, or **Done**).
