odoo.define(
    "ssi_l10n_id_taxform_coretax_bupot_21_payslip_batch.hr_payslip_batch_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/hr_payslip_batch/20-export-coretax.md
        //
        // Boundary (patterns.md §Q): this tour only proves the button opens
        // the Export Coretax PPh 21 Withholding XML wizard, then closes it
        // via Discard. It never selects a salary rule nor clicks the
        // wizard's own Export button, because the resulting action is an
        // ir.actions.report (qweb-xml) download with no DOM "finished"
        // signal — clicking through it could hang headless Chrome. The
        // export logic itself (which payslips are included, the field
        // mapping) is covered by tests/test_coretax_bupot_21.py instead.
        tour.register(
            "ssi_l10n_id_taxform_coretax_bupot_21_payslip_batch_hr_payslip_batch_export_coretax",
            {
                test: true,
                url: "/web",
            },
            [
                // ── Flow 1 — Open the Human Resource > Payroll > Payslip
                // Batches menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Human Resource app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
                },
                {
                    content: "Open the Payroll menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_hr_payroll.hr_payroll_root_menu"]',
                },
                {
                    content: "Open the Payslip Batches menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_hr_payroll_batch.hr_payslip_batch_menu"]',
                },
                {
                    content: "Payslip Batches list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payslip Batches)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 2 — Open the batch to export. The Pre-Condition
                // record (status Done) is prepared in setUpClass and
                // carries the type "TOUR BATCH EXPORT CORETAX".
                {
                    content: "Open the batch",
                    trigger:
                        ".o_data_row:contains(TOUR BATCH EXPORT CORETAX) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Batch form is displayed",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // ── Flow 3 — On the Payslips tab, click the Export
                // Coretax PPh 21 XML button.
                // The button is type="action" — its "name" attribute is a
                // numeric window action id resolved at render time, so it
                // is targeted by its visible label (selectors.md §4).
                {
                    content: "Open the Payslips tab",
                    trigger: ".o_notebook .nav-link:contains(Payslips)",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Click the Export Coretax PPh 21 XML button",
                    trigger:
                        ".o_form_view button:enabled:contains('Export Coretax PPh 21 XML')",
                    extra_trigger: ".o_form_view",
                },

                // ── Boundary — the wizard is proven open, then closed.
                // Flow 4 (select the salary rules) and Flow 5 (click
                // Export) are intentionally NOT executed — see the module
                // docstring above.
                //
                // 14.0: do NOT prefix the trigger with ".modal" — when a
                // modal is displayed, web_tour scopes the search to
                // $modal_displayed.find(trigger), and $modal_displayed
                // already IS the ".modal" element (patterns.md §H).
                {
                    content:
                        "The Export Coretax PPh 21 Withholding XML wizard is displayed",
                    trigger: ".modal-title:contains('Export Coretax PPh 21 XML')",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Discard the wizard",
                    trigger: ".modal-footer button.btn-secondary",
                    in_modal: true,
                },

                // ── Post-Condition (tour boundary) — the wizard is closed
                // and the batch form is displayed again. Whether an XML
                // file is actually generated and downloaded is out of tour
                // scope.
                {
                    content: "Wizard is closed and the batch form is displayed",
                    trigger: ".o_form_view",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
