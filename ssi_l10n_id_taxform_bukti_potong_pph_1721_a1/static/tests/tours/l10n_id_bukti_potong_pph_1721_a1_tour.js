/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

odoo.define(
    "ssi_l10n_id_taxform_bukti_potong_pph_1721_a1.l10n_id_bukti_potong_pph_1721_a1_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // ── Menu: Taxform > Bukti Potong > Tax Form 1721 A1 (Flow step 1
        // of every IK in this file).
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
                content: "Open the Tax Form 1721 A1 menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_l10n_id_taxform_bukti_potong_pph_1721_a1.bukti_potong_pph_1721_a1_menu"]',
            },
            {
                content: "Tax Form 1721 A1 list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Tax Form 1721 A1)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },
        ];

        // Opens the record whose Wajib Pajak column contains `wpName`,
        // then (14.0 only) clicks Edit so the fields become editable.
        function openRecordSteps(wpName, withEdit) {
            var steps = [
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
            if (withEdit) {
                steps.push(
                    {
                        content: "Click the Edit button",
                        trigger: ".o_form_button_edit",
                    },
                    {
                        content: "Form is now editable",
                        trigger: ".o_form_view.o_form_editable",
                        run: function () {
                            // Assertion only.
                        },
                    }
                );
            }
            return steps;
        }

        // Selects `wpName` on the Wajib Pajak many2one, which triggers
        // onchange_wajib_pajak_id and auto-fills the identity fields.
        function selectWajibPajakSteps(wpName) {
            return [
                {
                    content: "Select the Wajib Pajak",
                    trigger: ".o_field_many2one[name='wajib_pajak_id'] input",
                    run: "text " + wpName,
                },
                {
                    content: "Pick the Wajib Pajak from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(" + wpName + ")",
                    in_modal: false,
                },
            ];
        }

        // Selects `label` on the Kode Objek Pajak many2one.
        function selectKodeObjekPajakSteps(label) {
            return [
                {
                    content: "Select the Kode Objek Pajak",
                    trigger: ".o_field_many2one[name='kode_objek_pajak_id'] input",
                    run: "text " + label,
                },
                {
                    content: "Pick the Kode Objek Pajak from the dropdown",
                    trigger: ".ui-autocomplete .ui-menu-item a:contains(" + label + ")",
                    in_modal: false,
                },
            ];
        }

        // Selects `periodName` on both the Period Awal and Period Akhir
        // many2one fields.
        function selectPeriodSteps(periodName) {
            return [
                {
                    content: "Select the Period Awal",
                    trigger: ".o_field_many2one[name='start_tax_period_id'] input",
                    run: "text " + periodName,
                },
                {
                    content: "Pick the Period Awal from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(" + periodName + ")",
                    in_modal: false,
                },
                {
                    content: "Select the Period Akhir",
                    trigger: ".o_field_many2one[name='end_tax_period_id'] input",
                    run: "text " + periodName,
                },
                {
                    content: "Pick the Period Akhir from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(" + periodName + ")",
                    in_modal: false,
                },
            ];
        }

        // The field selected just before Save (Wajib Pajak on edit,
        // Period Akhir on create) triggers an onchange RPC that
        // recomputes several other fields on this model. `extra_trigger`
        // holds the click until `body` no longer carries the `oe_wait`
        // class Loading.on_rpc_event() (web/static/src/js/chrome/
        // loading.js) adds the instant a non-shadow RPC is dispatched
        // and removes the instant it completes -- unlike the 3s-delayed
        // `o_ui_blocked`, this reflects any RPC immediately, so it is a
        // true gate rather than one that matches seconds too late. Without
        // it, Save can race ahead of that onchange and the record never
        // reaches the readonly Post-Condition below (CI run 33072927047,
        // "Invalid fields: Period Akhir" logged 9ms after Save was
        // clicked -- see issue #230).
        var saveSteps = [
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
                extra_trigger: "body:not(.oe_wait)",
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

        // ── IK: docs/l10n_id_bukti_potong_pph_1721_a1/01-create.md
        tour.register(
            "ssi_l10n_id_taxform_bukti_potong_pph_1721_a1_l10n_id_bukti_potong_pph_1721_a1_create",
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
                selectWajibPajakSteps("TOUR WP Create1721A1"),
                selectKodeObjekPajakSteps("Pegawai Tetap"),
                selectPeriodSteps("TOUR 01/2026"),
                // ── Flow 8 — Click Save.
                saveSteps,
                // ── Post-Condition — a new record is created in Draft. In
                // 14.0, Save keeps the form open in read-only mode (it does
                // not navigate back to the list), so what is asserted here
                // is the saved data shown on the form itself, not a list
                // row.
                [
                    {
                        content: "Wajib Pajak shows the created value",
                        trigger:
                            ".o_form_readonly .o_field_widget[name='wajib_pajak_id']:contains(TOUR WP Create1721A1)",
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

        // ── IK: docs/l10n_id_bukti_potong_pph_1721_a1/02-edit.md
        tour.register(
            "ssi_l10n_id_taxform_bukti_potong_pph_1721_a1_l10n_id_bukti_potong_pph_1721_a1_edit",
            {test: true, url: "/web"},
            [].concat(
                openMenuSteps,
                // ── Flow 2 — Find and open the record to edit.
                openRecordSteps("TOUR WP EditSource1721A1", true),
                // ── Flow 3/4 — Change Wajib Pajak, which re-fills the
                // identity fields from the newly selected partner.
                selectWajibPajakSteps("TOUR WP EditTarget1721A1"),
                // ── Flow 5 — Click Save.
                saveSteps,
                // ── Post-Condition — record updated with the new value.
                [
                    {
                        content: "Go back to the list",
                        trigger:
                            ".breadcrumb-item.o_back_button a:contains(Tax Form 1721 A1)",
                    },
                    {
                        content: "Reopen the record",
                        trigger: ".o_data_row:contains(TOUR WP EditTarget1721A1)",
                    },
                    {
                        content: "Wajib Pajak shows the new value",
                        trigger:
                            ".o_form_readonly .o_field_widget[name='wajib_pajak_id']:contains(TOUR WP EditTarget1721A1)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // ── IK: docs/l10n_id_bukti_potong_pph_1721_a1/03-delete.md
        tour.register(
            "ssi_l10n_id_taxform_bukti_potong_pph_1721_a1_l10n_id_bukti_potong_pph_1721_a1_delete",
            {test: true, url: "/web"},
            [].concat(
                openMenuSteps,
                // ── Flow 2 — Open the record to delete.
                openRecordSteps("TOUR WP Delete1721A1", false),
                // ── Flow 3 — Click Action > Delete.
                [
                    {
                        content: "Open the Action menu",
                        trigger: ".o_cp_action_menus button:contains(Action)",
                    },
                    {
                        content: "Click Delete",
                        trigger: ".o_cp_action_menus .o_menu_item a",
                        run: function () {
                            var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                                function () {
                                    return $(this).text().trim() === "Delete";
                                }
                            );
                            $delete[0].click();
                        },
                    },
                    // ── Flow 4 — Click OK to confirm.
                    {
                        content: "Confirm deletion",
                        trigger: ".modal-footer button.btn-primary",
                        in_modal: true,
                    },
                    {
                        content: "Click the [List] breadcrumb to return to the list",
                        trigger:
                            ".breadcrumb-item.o_back_button a:contains(Tax Form 1721 A1)",
                    },
                ],
                // ── Post-Condition — record no longer in the list.
                [
                    {
                        content: "Record is no longer in the list",
                        trigger:
                            ".o_list_view:not(:has(.o_data_row:contains(TOUR WP Delete1721A1)))",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // ── IK: docs/l10n_id_bukti_potong_pph_1721_a1/04-confirm.md
        tour.register(
            "ssi_l10n_id_taxform_bukti_potong_pph_1721_a1_l10n_id_bukti_potong_pph_1721_a1_confirm",
            {test: true, url: "/web"},
            [].concat(
                openMenuSteps,
                // ── Flow 2 — Open the record to confirm.
                openRecordSteps("TOUR WP Confirm1721A1", false),
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

        // ── IK: docs/l10n_id_bukti_potong_pph_1721_a1/05-approve.md
        tour.register(
            "ssi_l10n_id_taxform_bukti_potong_pph_1721_a1_l10n_id_bukti_potong_pph_1721_a1_approve",
            {test: true, url: "/web"},
            [].concat(
                openMenuSteps,
                // ── Flow 2 — Open the record to approve.
                openRecordSteps("TOUR WP Approve1721A1", false),
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

        // ── IK: docs/l10n_id_bukti_potong_pph_1721_a1/06-reject.md
        tour.register(
            "ssi_l10n_id_taxform_bukti_potong_pph_1721_a1_l10n_id_bukti_potong_pph_1721_a1_reject",
            {test: true, url: "/web"},
            [].concat(
                openMenuSteps,
                // ── Flow 2 — Open the record to reject.
                openRecordSteps("TOUR WP Reject1721A1", false),
                // ── Flow 3 — Click the Reject button.
                [
                    {
                        content: "Click the Reject button",
                        trigger:
                            ".o_statusbar_buttons button[name='action_reject_approval']",
                        extra_trigger: ".o_form_view",
                    },
                    // ── Flow 4 — Click OK on the confirmation dialog.
                    confirmDialogStep,
                ],
                // ── Post-Condition — status changes to Rejected.
                [
                    {
                        content: "Status is Rejected",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='reject'].btn-primary",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // ── IK: docs/l10n_id_bukti_potong_pph_1721_a1/10-cancel.md
        tour.register(
            "ssi_l10n_id_taxform_bukti_potong_pph_1721_a1_l10n_id_bukti_potong_pph_1721_a1_cancel",
            {test: true, url: "/web"},
            [].concat(
                openMenuSteps,
                // ── Flow 2 — Open the record to cancel.
                openRecordSteps("TOUR WP Cancel1721A1", false),
                // ── Flow 3 — Click the Cancel button.
                //
                // The Cancel button is type="action" with the wizard's
                // numeric action id as `name` (resolved from
                // "%(...)d" at view compile time), so it cannot be
                // targeted by `name=`. Target it by its visible label
                // instead, like the Delete action-menu item above.
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
                            ".o_field_widget[name='cancel_reason_id'] label:contains(TOUR Cancel Reason 1721A1)",
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

        // ── IK: docs/l10n_id_bukti_potong_pph_1721_a1/12-restart.md
        tour.register(
            "ssi_l10n_id_taxform_bukti_potong_pph_1721_a1_l10n_id_bukti_potong_pph_1721_a1_restart",
            {test: true, url: "/web"},
            [].concat(
                openMenuSteps,
                // ── Flow 2 — Open the record to restart.
                openRecordSteps("TOUR WP Restart1721A1", false),
                // ── Flow 3 — Click the Restart button.
                [
                    {
                        content: "Click the Restart button",
                        trigger: ".o_statusbar_buttons button[name='action_restart']",
                        extra_trigger: ".o_form_view",
                    },
                    // ── Flow 4 — Click OK on the confirmation dialog.
                    confirmDialogStep,
                ],
                // ── Post-Condition — status returns to Draft.
                [
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

        // ── IK: docs/l10n_id_bukti_potong_pph_1721_a1/14-restart-approval.md
        tour.register(
            "ssi_l10n_id_taxform_bukti_potong_pph_1721_a1_l10n_id_bukti_potong_pph_1721_a1_restart_approval",
            {test: true, url: "/web"},
            [].concat(
                openMenuSteps,
                // ── Flow 2 — Open the record whose approval process
                // needs to be restarted.
                openRecordSteps("TOUR WP RestartAppr1721A1", false),
                // ── Flow 3 — Click the Restart Approval Process button.
                [
                    {
                        content: "Click the Restart Approval Process button",
                        trigger:
                            ".o_statusbar_buttons button[name='action_reload_approval_template']",
                        extra_trigger: ".o_form_view",
                    },
                    // ── Flow 4 — Click OK on the confirmation dialog.
                    confirmDialogStep,
                ],
                // ── Post-Condition — status remains Waiting for
                // Approval.
                [
                    {
                        content: "Status is still Waiting for Approval",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );
    }
);
