/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

odoo.define(
    "ssi_l10n_id_taxform_bukti_potong_pph_f113302_work_log." +
        "l10n_id_bukti_potong_pph_f113302_out_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Types `label` into the many2one `fieldName` and picks it
        // from the autocomplete dropdown.
        function selectMany2oneSteps(fieldName, label) {
            return [
                {
                    content: "Select " + label + " on " + fieldName,
                    trigger: ".o_field_many2one[name='" + fieldName + "'] input",
                    run: "text " + label,
                },
                {
                    content: "Pick " + label + " from the dropdown",
                    trigger: ".ui-autocomplete .ui-menu-item a:contains(" + label + ")",
                    in_modal: false,
                },
            ];
        }

        // IK: docs/l10n_id_bukti_potong_pph_f113302_out/01-create.md
        // (E2a delta -- Modified Flow). Navigation and field-filling
        // steps are retraced from the base IK
        // ssi_l10n_id_taxform_bukti_potong_pph_f113302/docs/
        // l10n_id_bukti_potong_pph_f113302_out/01-create.md Flow
        // steps 1-5 -- see skill odoo-development-ui-test,
        // scope-and-boundaries.md §3 ("Backing dua file: tour
        // extension = base IK ∪ delta IK"). The delta assertion,
        // inserted right after the base's Flow step 2 (Click New),
        // proves the additional "Work Log" page is already rendered
        // on the unsaved create form, before any required field is
        // filled.
        tour.register(
            "ssi_l10n_id_taxform_bukti_potong_pph_f113302_work_log_" +
                "l10n_id_bukti_potong_pph_f113302_out_create",
            {test: true, url: "/web"},
            [].concat(
                // ── Base Flow 1 — Open the Taxform > Bukti Potong >
                // PPh 21 Final (f.1.1.33.02) Out menu.
                [
                    tour.stepUtils.showAppsMenuItem(),
                    {
                        content: "Open the Taxform app",
                        trigger:
                            '.o_app[data-menu-xmlid="ssi_l10n_id_taxform.taxform_main_menu"]',
                    },
                    {
                        content: "Open the Bukti Potong menu",
                        trigger:
                            '.o_menu_sections [data-menu-xmlid="ssi_l10n_id_taxform.taxform_bukti_potong_menu"]',
                    },
                    {
                        content: "Open the PPh 21 Final (f.1.1.33.02) Out menu",
                        trigger:
                            '.o_menu_sections [data-menu-xmlid="ssi_l10n_id_taxform_bukti_potong_pph_f113302.bukti_potong_pph_21_out_menu"]',
                    },
                    {
                        content: "PPh 21 Final (f.1.1.33.02) Out list is displayed",
                        trigger:
                            ".o_control_panel .breadcrumb-item.active:contains(PPh 21 Final)",
                        extra_trigger: ".o_list_view",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ],
                // ── Base Flow 2 — Click the New button.
                [
                    {
                        content: "Click Create",
                        trigger: ".o_list_button_add",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open in edit mode",
                        trigger: ".o_form_view.o_form_editable",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ],
                // ── Delta anchor — right after the base's Flow step
                // 2, before any required field is filled.
                [
                    {
                        content: "Open the Work Log tab",
                        trigger: ".o_notebook .nav-link:contains(Work Log)",
                    },
                    {
                        // Anchored to the field label, not the float
                        // widget itself -- a label always carries
                        // text regardless of the field's value
                        // (odoo-development-ui-test skill,
                        // patterns.md §O).
                        content: "Work Log page shows the Estimation field",
                        trigger: ".o_form_label:contains(Estimation)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ],
                // ── Base Flow 3 — Fill in the required fields.
                selectMany2oneSteps("tax_period_id", "TOUR 06/2026 F113302WL"),
                selectMany2oneSteps("journal_id", "PPh 21 Final Out - (test)"),
                selectMany2oneSteps(
                    "account_id",
                    "Art. 21 Final Payable No Taxform - (test)"
                ),
                selectMany2oneSteps("kpp_id", "TOUR KPP F113302WL"),
                selectMany2oneSteps("wajib_pajak_id", "TOUR WP CreateF113302WL"),
                selectMany2oneSteps("ttd_id", "TOUR TTD F113302WL"),
                // ── Base Flow 5 — Click Save.
                [
                    {
                        content: "Save the record",
                        trigger: ".o_form_button_save",
                    },
                    {
                        content: "Record is saved",
                        trigger: ".o_form_view.o_form_readonly",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ],
                // ── Base Post-Condition — a new record is created in
                // Draft. In 14.0, Save keeps the form open in
                // read-only mode (it does not navigate back to the
                // list), so what is asserted here is the saved data
                // shown on the form itself, not a list row.
                [
                    {
                        content: "Wajib Pajak shows the created value",
                        trigger:
                            ".o_form_readonly .o_field_widget[name='wajib_pajak_id']:contains(TOUR WP CreateF113302WL)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        content: "Status is Draft",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );
    }
);
