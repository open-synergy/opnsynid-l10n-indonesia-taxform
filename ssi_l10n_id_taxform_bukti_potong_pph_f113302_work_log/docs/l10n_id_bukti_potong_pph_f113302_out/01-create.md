# Create Bukti Potong PPh f.1.1.33.02 Out

> **Module:** ssi_l10n_id_taxform_bukti_potong_pph_f113302_work_log
>
> **Extends:** ssi_l10n_id_taxform_bukti_potong_pph_f113302 — model
> `l10n_id.bukti_potong_pph_f113302_out`, aksi `01-create`

## Modified Flow

- Anchor: on Flow base step 2 (Click the **New** button. **(14.0: "Create")**). This
  module adds a **Work Log** page to the form (inserted after the last existing tab),
  showing **Estimation**, **Total**, **Remaining**, and **Excess** hour fields, the
  **Work Log Analytic Account** field, and the list of work log entries (`hr.work_log`)
  linked to this document. The page is already rendered on the unsaved create form — no
  field needs to be filled and no state condition applies.
- This document goes straight from **Waiting for Approval** to **Done** once the last
  approval level is fulfilled (see base `05-approve`) — there is no separate **On
  Progress** working period. The page is not gated by document status: it can be opened
  and filled while the record is in any state, starting from **Draft** — the state this
  Create flow produces.
