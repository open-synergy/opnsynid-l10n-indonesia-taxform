/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

odoo.define(
    "ssi_l10n_id_taxform_bukti_potong_pph_f113304." +
        "l10n_id_bukti_potong_pph_f113304_out_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // ── Menu: Taxform > Bukti Potong > PPh 22 (f.1.1.33.04) Out
        // (Flow step 1 of every IK in this file).
        var openMenuSteps = [
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
                content: "Open the PPh 22 (f.1.1.33.04) Out menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_l10n_id_taxform_bukti_potong_pph_f113304.bukti_potong_pph_22_out_menu"]',
            },
            {
                content: "PPh 22 (f.1.1.33.04) Out list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(PPh 22)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },
        ];

        // Opens the record whose Wajib Pajak column contains `wpName`.
        function openRecordSteps(wpName) {
            return [
                {
                    content: "Open the record",
                    trigger: ".o_data_row:contains(" + wpName + ") .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },
            ];
        }

        // Types `label` into the many2one `fieldName` and picks it from
        // the autocomplete dropdown.
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

        var saveSteps = [
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
        ];

        var confirmDialogStep = {
            content: "Confirm the dialog",
            trigger: ".modal-footer button.btn-primary",
            in_modal: true,
        };

        // ── IK: docs/l10n_id_bukti_potong_pph_f113304_out/01-create.md
        tour.register(
            "ssi_l10n_id_taxform_bukti_potong_pph_f113304_" +
                "l10n_id_bukti_potong_pph_f113304_out_create",
            {test: true, url: "/web"},
            [].concat(
                openMenuSteps,
                // ── Flow 2 — Click the New button.
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
                // ── Flow 3 — Fill in the required fields.
                selectMany2oneSteps("tax_period_id", "TOUR 06/2026 F113304 Out"),
                selectMany2oneSteps("journal_id", "PPh 22 Out - (test)"),
                selectMany2oneSteps(
                    "account_id",
                    "Art. 22 Payable No Taxform - (test)"
                ),
                selectMany2oneSteps("kpp_id", "TOUR KPP F113304 Out"),
                selectMany2oneSteps("wajib_pajak_id", "TOUR WP CreateF113304O"),
                selectMany2oneSteps("ttd_id", "TOUR TTD F113304 Out"),
                // ── Flow 5 — Click Save.
                saveSteps,
                // ── Post-Condition — a new record is created in Draft.
                // In 14.0, Save keeps the form open in read-only mode
                // (it does not navigate back to the list), so what is
                // asserted here is the saved data shown on the form
                // itself, not a list row.
                [
                    {
                        content: "Wajib Pajak shows the created value",
                        trigger:
                            ".o_form_readonly .o_field_widget[name='wajib_pajak_id']:contains(TOUR WP CreateF113304O)",
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

        // ── IK: docs/l10n_id_bukti_potong_pph_f113304_out/04-confirm.md
        tour.register(
            "ssi_l10n_id_taxform_bukti_potong_pph_f113304_" +
                "l10n_id_bukti_potong_pph_f113304_out_confirm",
            {test: true, url: "/web"},
            [].concat(
                openMenuSteps,
                // ── Flow 2 — Open the record to confirm.
                openRecordSteps("TOUR WP ConfirmF113304O"),
                // ── Flow 3 — Click the Confirm button.
                [
                    {
                        content: "Click the Confirm button",
                        trigger: ".o_statusbar_buttons button[name='action_confirm']",
                        extra_trigger: ".o_form_view",
                    },
                    // ── Flow 4 — Click OK on the confirmation dialog.
                    confirmDialogStep,
                ],
                // ── Post-Condition — status changes to Waiting for
                // Approval.
                [
                    {
                        content: "Status is Waiting for Approval",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // ── IK: docs/l10n_id_bukti_potong_pph_f113304_out/05-approve.md
        tour.register(
            "ssi_l10n_id_taxform_bukti_potong_pph_f113304_" +
                "l10n_id_bukti_potong_pph_f113304_out_approve",
            {test: true, url: "/web"},
            [].concat(
                openMenuSteps,
                // ── Flow 2 — Open the record to approve.
                openRecordSteps("TOUR WP ApproveF113304O"),
                // ── Flow 3 — Click the Approve button.
                [
                    {
                        content: "Click the Approve button",
                        trigger:
                            ".o_statusbar_buttons button[name='action_approve_approval']",
                        extra_trigger: ".o_form_view",
                    },
                    // ── Flow 4 — Click OK on the confirmation dialog.
                    confirmDialogStep,
                ],
                // ── Post-Condition — single approval level, so the
                // document is finished automatically: status is Done.
                [
                    {
                        content: "Status is Done",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // ── IK: docs/l10n_id_bukti_potong_pph_f113304_out/10-cancel.md
        tour.register(
            "ssi_l10n_id_taxform_bukti_potong_pph_f113304_" +
                "l10n_id_bukti_potong_pph_f113304_out_cancel",
            {test: true, url: "/web"},
            [].concat(
                openMenuSteps,
                // ── Flow 2 — Open the record to cancel.
                openRecordSteps("TOUR WP CancelF113304O"),
                // ── Flow 3 — Click the Cancel button.
                //
                // The Cancel button is type="action" with the wizard's
                // numeric action id as `name` (resolved from
                // "%(...)d" at view compile time), so it cannot be
                // targeted by `name=`. Target it by its visible label
                // instead.
                [
                    {
                        content: "Click the Cancel button",
                        trigger: ".o_statusbar_buttons button",
                        extra_trigger: ".o_form_view",
                        run: function () {
                            var $cancel = $(".o_statusbar_buttons button").filter(
                                function () {
                                    return $(this).text().trim() === "Cancel";
                                }
                            );
                            $cancel[0].click();
                        },
                    },
                    {
                        content: "Cancel wizard is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    // ── Flow 4 — Select the Cancellation Reason.
                    {
                        content: "Select the cancellation reason",
                        trigger:
                            ".o_field_widget[name='cancel_reason_id'] label:contains(TOUR Cancel Reason F113304 Out)",
                    },
                    // ── Flow 5 — Click Confirm.
                    {
                        content: "Confirm the wizard",
                        trigger: ".modal-footer button[name='action_confirm']",
                    },
                    // ── Flow 6 — Click OK on the confirmation dialog.
                    confirmDialogStep,
                ],
                // ── Post-Condition — status changes to Cancelled.
                [
                    {
                        content: "Status is Cancelled",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );
    }
);
