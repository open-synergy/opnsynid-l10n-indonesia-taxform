// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_l10n_id_taxform.l10n_id_tax_year_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Taxform > Configuration > Tax Periods > Tax
    // Years. "Tax Periods" (level 3, taxform_period_conf_menu) has
    // children of its own (this menu's "Tax Years" leaf, and its sibling
    // "Tax Periods" leaf) and is therefore rendered as a non-clickable
    // dropdown header with no data-menu-xmlid -- only the leaf "Tax
    // Years" item gets a step (see odoo-development-ui-test skill,
    // patterns-navigation-and-form.md §A).
    function openTaxYearMenuSteps() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Taxform app",
                trigger:
                    '.o_app[data-menu-xmlid="ssi_l10n_id_taxform.taxform_main_menu"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_l10n_id_taxform.taxform_configuration_menu"]',
            },
            {
                content: "Open the Tax Years menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_l10n_id_taxform.tax_year_menu"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view --
                // the app landing action is also a .o_list_view.
                content: "Tax Years list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Tax Years)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/l10n_id_tax_year/01-create.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_l10n_id_taxform_l10n_id_tax_year_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTaxYearMenuSteps(), [
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
                    // Assertion only; do not trigger the default click action.
                },
            },
            // ── Flow 3 — Fill in Tax Year, Code, Date Start, Date End.
            {
                content: "Fill in Tax Year",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-TY-CREATE-UI",
            },
            {
                content: "Fill in Code",
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TY-CREATE-01",
            },
            {
                content: "Fill in Date Start",
                trigger: ".o_field_widget[name='date_start'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 01/01/2030",
            },
            {
                content: "Fill in Date End",
                trigger: ".o_field_widget[name='date_end'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 12/31/2030",
            },
            // ── Flow 4 — Note is optional; left blank.
            // ── Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            // ── Post-Condition — a new tax year record is created, active
            // by default, with an empty Periods list.
            {
                content: "Back to the Tax Years list",
                trigger: ".breadcrumb-item.o_back_button a:contains(Tax Years)",
            },
            {
                content: "New record appears in the list",
                trigger: ".o_data_row:contains(TOUR-TY-CREATE-UI)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/l10n_id_tax_year/02-edit.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_l10n_id_taxform_l10n_id_tax_year_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTaxYearMenuSteps(), [
            // ── Flow 2 — Find and open the record to edit.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-TY-EDIT-UI) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            // 14.0 — a record opened from the list is read-only; edit
            // requires an explicit click first.
            {
                content: "Click the Edit button",
                trigger: ".o_form_button_edit",
            },
            {
                content: "Form is now editable",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            // ── Flow 3 — Change Date End.
            {
                content: "Change Date End",
                trigger: ".o_field_widget[name='date_end'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text_blur 12/25/2028",
            },
            // ── Flow 4 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            // ── Post-Condition — the record is updated with the new values.
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/l10n_id_tax_year/03-delete.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_l10n_id_taxform_l10n_id_tax_year_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTaxYearMenuSteps(), [
            // ── Flow 2-4 — select the record and delete it, from the
            // record's own form. The 14.0 list-selector checkbox is
            // flaky (odoo-development-ui-test skill,
            // patterns-dialogs-and-wizards.md §I); opening the record
            // and deleting from its own Action menu reaches the same
            // Post-Condition.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-TY-DELETE-UI) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Delete",
                // Action menu items are Owl components; target the <a>
                // inside .o_menu_item and match the exact label so
                // :contains(Delete) as a substring never picks "Archive".
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
            {
                content: "Confirm deletion",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Back to the Tax Years list",
                trigger: ".breadcrumb-item.o_back_button a:contains(Tax Years)",
            },
            // ── Post-Condition — the record is permanently removed.
            {
                content: "Deleted tax year no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(" +
                    ".o_data_row:contains(TOUR-TY-DELETE-UI)))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/l10n_id_tax_year/04-create-period.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_l10n_id_taxform_l10n_id_tax_year_create_period",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTaxYearMenuSteps(), [
            // ── Flow 2 — Open the tax year record to generate periods
            // for. Its Periods list starts empty (setUpClass creates it
            // with no period_ids), which is what makes the gate below
            // valid (patterns-advanced-gotchas.md §P litmus test).
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-TY-PERIOD-UI) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            // ── Flow 3 — In the header, click Create Period.
            // extra_trigger: ".o_form_view" is mandatory on every
            // header/statusbar button click, with or without a dialog
            // (odoo-development-ui-test skill,
            // patterns-dialogs-and-wizards.md §F).
            {
                content: "Click the Create Period button",
                trigger: ".o_statusbar_buttons button[name='action_create_period']",
                extra_trigger: ".o_form_view",
            },
            // ── Post-Condition — one l10n_id.tax_period record is
            // created for each calendar month between Date Start and
            // Date End. Gate on the first and last generated periods:
            // these rows cannot exist before Create Period is clicked
            // (the fixture's Periods list starts empty), so their
            // presence is proof the button's effect landed -- without
            // asserting the exact row count, which is the unit test's
            // job (tests/test_data_l10n_id_taxform.yaml).
            {
                content: "The January 2031 period is generated",
                trigger:
                    ".o_field_x2many[name='period_ids'] " +
                    ".o_data_row:contains(01/2031)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "The December 2031 period is generated",
                trigger:
                    ".o_field_x2many[name='period_ids'] " +
                    ".o_data_row:contains(12/2031)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );
});
