// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_l10n_id_taxform_faktur_pajak_klipajak.klikpajak_backend_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Shared navigation block reused by every tour below. It corresponds
        // to Flow 1 of every klikpajak_backend IK: "Open the Settings >
        // Technical > Klik Pajak > Backends menu."
        //
        // The path has four levels but only three are clickable steps.
        // "Settings" is the app icon. "Technical" (base.menu_custom) is a
        // direct child of the app root, so it is always rendered as its own
        // top-nav dropdown section. "Klik Pajak" (klikpajak_configuration_menu)
        // is one level deeper, carries no action of its own, and has one
        // child ("Backends") -- 14.0 therefore renders it as a
        // .dropdown-header with no data-menu-xmlid and flattens "Backends"
        // into the same "Technical" dropdown (odoo-development-ui-test
        // patterns.md §A).
        function openKlikpajakBackendList() {
            return [
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Settings app",
                    trigger: '.o_app[data-menu-xmlid="base.menu_administration"]',
                },
                {
                    content: "Open the Technical menu",
                    trigger: '.o_menu_sections [data-menu-xmlid="base.menu_custom"]',
                },
                {
                    content: "Open the Backends menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_l10n_id_taxform_faktur_pajak_klipajak.klikpajak_backend_menu"]',
                },
                {
                    // Gate: wait for the TARGET action to be installed, not
                    // just for "a list is on screen" (odoo-development-ui-test
                    // patterns.md §A).
                    content: "Klik Pajak Backends list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Klik Pajak Backends)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ];
        }

        // IK: docs/klikpajak_backend/01-create.md
        tour.register(
            "ssi_l10n_id_taxform_faktur_pajak_klipajak_klikpajak_backend_create",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // ── Flow 1 — Open the Backends menu.
                openKlikpajakBackendList(),
                [
                    // ── Flow 2 — Click the New button.
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

                    // ── Flow 3 — Fill in the required fields (Name, Code,
                    // Base URL; the four API endpoint paths keep their
                    // defaults).
                    {
                        content: "Fill in Name",
                        trigger: ".o_field_widget[name='name']",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text TOUR KLIKPAJAK BACKEND Create",
                    },
                    {
                        content: "Leave Code as /",
                        trigger: ".o_field_widget[name='code']",
                        run: "text /",
                    },
                    {
                        content: "Fill in Base URL",
                        trigger: ".o_field_widget[name='base_url']",
                        run: "text https://sandbox.klikpajak.id",
                    },

                    // ── Flow 4 — On the Authentication tab, keep the default
                    // HMAC method and fill Client ID and Client Secret.
                    {
                        content: "Open the Authentication tab",
                        trigger: ".o_notebook .nav-link:contains(Authentication)",
                    },
                    {
                        content: "Fill in Client ID",
                        trigger: ".o_field_widget[name='client_id']",
                        run: "text tour-client-id",
                    },
                    {
                        content: "Fill in Client Secret",
                        trigger: ".o_field_widget[name='client_secret']",
                        run: "text tour-client-secret",
                    },

                    // ── Flow 5 — On the Parameters tab, add a parameter row
                    // (Skenario Uji: "isi baris parameter").
                    {
                        content: "Open the Parameters tab",
                        trigger: ".o_notebook .nav-link:contains(Parameters)",
                    },
                    {
                        content: "Add a parameter line",
                        trigger: ".o_field_x2many_list_row_add a",
                        extra_trigger: ".o_form_view.o_form_editable",
                    },
                    {
                        content: "Fill in Parameter Name",
                        trigger: ".o_selected_row .o_field_widget[name='name']",
                        run: "text TOUR_PARAM",
                    },
                    {
                        content: "Fill in Value",
                        trigger: ".o_selected_row .o_field_widget[name='value']",
                        run: "text tour-value",
                    },
                    {
                        // Commit the row by clicking a field outside the
                        // x2many editable list -- NOT press Tab
                        // (odoo-development-ui-test patterns-fields.md §C
                        // "Jebakan 2").
                        content: "Commit the parameter row",
                        trigger: ".o_field_widget[name='code']",
                        run: "click",
                    },

                    // ── Flow 6 — Click Save.
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

                    // ── Post-Condition — A new record is created in Draft
                    // status.
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

        // IK: docs/klikpajak_backend/02-edit.md
        tour.register(
            "ssi_l10n_id_taxform_faktur_pajak_klipajak_klikpajak_backend_edit",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // ── Flow 1 — Open the Backends menu.
                openKlikpajakBackendList(),
                [
                    // ── Flow 2 — Find and open the record to edit.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR KLIKPAJAK BACKEND Edit) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Record is open (read-only)",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    // 14.0 opens an existing record read-only -- click Edit
                    // before touching any field (odoo-development-ui-test
                    // patterns.md §E).
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
                    },

                    // ── Flow 3 — Change Base URL.
                    {
                        content: "Change Base URL",
                        trigger: ".o_field_widget[name='base_url']",
                        run: "text https://sandbox.klikpajak.id/edited",
                    },

                    // ── Flow 4 — On the Parameters tab, edit the existing
                    // parameter row's Value (same tab as during creation).
                    {
                        content: "Open the Parameters tab",
                        trigger: ".o_notebook .nav-link:contains(Parameters)",
                    },
                    // The o2m list row's <td> cells carry no [name]
                    // attribute in 14.0 -- only class/tabindex/title. Select
                    // the Value column by its position instead: the tree
                    // view declares <field name="name"/><field
                    // name="type"/><field name="value"/> in that order
                    // (views/klikpajak_backend_views.xml), so the Value cell
                    // is the third .o_data_cell of the row.
                    {
                        content: "Click the parameter row's Value cell",
                        trigger:
                            ".o_data_row:contains(TOUR_PARAM_EDIT) .o_data_cell:eq(2)",
                    },
                    {
                        content: "Change the Value",
                        trigger: ".o_selected_row .o_field_widget[name='value']",
                        run: "text new-tour-value",
                    },
                    {
                        content: "Commit the parameter row",
                        trigger: ".o_field_widget[name='code']",
                        run: "click",
                    },

                    // ── Flow 5 — Click Save.
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

                    // ── Post-Condition — The record is updated with the new
                    // values. m2o/char values just written are not readable
                    // while the form was still editable (Sizzle
                    // defaultValue), so leave and reopen the record
                    // (odoo-development-ui-test
                    // patterns-post-conditions-and-waiting.md §L).
                    {
                        content: "Go back to the list",
                        trigger:
                            ".breadcrumb-item.o_back_button a:contains(Klik Pajak Backends)",
                    },
                    {
                        content: "Reopen the record",
                        trigger:
                            ".o_data_row:contains(TOUR KLIKPAJAK BACKEND Edit) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Base URL shows the new value",
                        trigger:
                            ".o_form_readonly .o_field_widget[name='base_url']:contains(https://sandbox.klikpajak.id/edited)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/klikpajak_backend/03-delete.md
        tour.register(
            "ssi_l10n_id_taxform_faktur_pajak_klipajak_klikpajak_backend_delete",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // ── Flow 1 — Open the Backends menu.
                openKlikpajakBackendList(),
                [
                    // Delete from the record's own form (Action menu), not
                    // the list checkbox -- the checkbox is flaky in 14.0
                    // (odoo-development-ui-test patterns.md §I).
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR KLIKPAJAK BACKEND Delete) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Record is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // ── Flow 2/3 — Click Action > Delete.
                    {
                        content: "Open the Action menu",
                        trigger: ".o_cp_action_menus button:contains(Action)",
                    },
                    {
                        content: "Click Delete",
                        // Owl menu item; match the label EXACTLY, not as a
                        // substring, so "Archive" is never picked instead.
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
                        content: "Go back to the list",
                        trigger:
                            ".breadcrumb-item.o_back_button a:contains(Klik Pajak Backends)",
                    },

                    // ── Post-Condition — The record no longer appears.
                    {
                        content: "Record no longer appears in the list",
                        trigger:
                            ".o_list_view:not(:has(.o_data_row:contains(TOUR KLIKPAJAK BACKEND Delete)))",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/klikpajak_backend/04-running.md
        tour.register(
            "ssi_l10n_id_taxform_faktur_pajak_klipajak_klikpajak_backend_running",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // ── Flow 1 — Open the Backends menu.
                openKlikpajakBackendList(),
                [
                    // ── Flow 2 — Find and open the record to run.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR KLIKPAJAK BACKEND Running) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Record is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // ── Flow 3 — Click the Running button. No confirm=
                    // dialog on this button, so no OK step here.
                    // extra_trigger is the mandatory settle gate for 14.0
                    // header-button clicks (odoo-development-ui-test
                    // patterns-dialogs-and-wizards.md §F) -- it does NOT by
                    // itself fix a dead click (step "succeeded" with no
                    // call_button RPC). The dead click this tour hit earlier
                    // was caused by empty required client_id/client_secret
                    // on the fixture record (auth_method defaults to
                    // "hmac"), which made Odoo's pre-action revalidation
                    // silently reject the click; fixed in
                    // tests/test_ui_klikpajak_backend.py _create_backend().
                    {
                        content: "Click the Running button",
                        trigger: ".o_statusbar_buttons button[name='action_running']",
                        extra_trigger: ".o_form_view",
                    },

                    // ── Post-Condition — Status changes to Running, and the
                    // Restart button becomes available (gate on the
                    // POST-write re-render, not on the click itself --
                    // odoo-development-ui-test
                    // patterns-post-conditions-and-waiting.md §P).
                    {
                        content: "Status is Running",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='running'].btn-primary",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        content: "Restart button is now available",
                        trigger:
                            ".o_statusbar_buttons button[name='action_restart']:enabled",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/klikpajak_backend/05-restart.md
        tour.register(
            "ssi_l10n_id_taxform_faktur_pajak_klipajak_klikpajak_backend_restart",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // ── Flow 1 — Open the Backends menu.
                openKlikpajakBackendList(),
                [
                    // ── Flow 2 — Find and open the record to restart.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR KLIKPAJAK BACKEND Restart) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Record is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // ── Flow 3 — Click the Restart button. No confirm=
                    // dialog on this button, so no OK step here. See the
                    // Running tour above for why extra_trigger is mandatory
                    // here and what actually caused the dead click.
                    {
                        content: "Click the Restart button",
                        trigger: ".o_statusbar_buttons button[name='action_restart']",
                        extra_trigger: ".o_form_view",
                    },

                    // ── Post-Condition — Status changes back to Draft, and
                    // the Running button becomes available again.
                    {
                        content: "Status is Draft",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        content: "Running button is now available",
                        trigger:
                            ".o_statusbar_buttons button[name='action_running']:enabled",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/klikpajak_backend/06-test-hmac.md
        tour.register(
            "ssi_l10n_id_taxform_faktur_pajak_klipajak_klikpajak_backend_test_hmac",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // ── Flow 1 — Open the Backends menu.
                openKlikpajakBackendList(),
                [
                    // ── Flow 2 — Find and open the record to test.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR KLIKPAJAK BACKEND Test HMAC) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Record is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // ── Flow 3 — Click the Test HMAC button. This action
                    // always raises a ValidationError to surface its
                    // result -- the dialog it opens is the EXPECTED
                    // outcome, not a tour failure (docs/klikpajak_backend/
                    // 06-test-hmac.md Post-Condition). extra_trigger is the
                    // mandatory settle gate for 14.0 header-button clicks
                    // (odoo-development-ui-test
                    // patterns-dialogs-and-wizards.md §F).
                    {
                        content: "Click the Test HMAC button",
                        trigger: ".o_statusbar_buttons button[name='action_get_hmac']",
                        extra_trigger: ".o_form_view",
                    },

                    // ── Post-Condition — A dialog shows the computed HMAC
                    // signature. Only the dialog TYPE (title "Validation
                    // Error", from the ValidationError -> WarningDialog
                    // mapping in web.CrashManager) is asserted here, not
                    // the signature value itself -- the tour verifies the
                    // result is surfaced to the user, not that the value
                    // is arithmetically correct (odoo-development-ui-test
                    // boundary: value correctness is unit-test territory).
                    {
                        content: "Result dialog is displayed",
                        trigger: ".modal-title:contains(Validation Error)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        content: "Close the dialog",
                        trigger: ".modal-footer button.btn-primary",
                        in_modal: true,
                    },
                    {
                        // Gerbang modal-tertutup wajib sesudah dialog
                        // (odoo-development-ui-test
                        // patterns-dialogs-and-wizards.md §G).
                        content: "Dialog is closed and the record is unchanged",
                        trigger: "body:not(:has(.modal))",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );
    }
);
