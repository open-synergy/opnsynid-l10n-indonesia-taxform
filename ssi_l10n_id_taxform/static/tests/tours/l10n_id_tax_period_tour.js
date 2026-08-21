// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_l10n_id_taxform.l10n_id_tax_period_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared opening steps: Taxform > Configuration > Tax Periods > Tax
    // Periods. "Tax Periods" (level 3, taxform_period_conf_menu) has
    // children of its own (its sibling "Tax Years" leaf, and this menu's
    // own "Tax Periods" leaf) and is therefore rendered as a
    // non-clickable dropdown header with no data-menu-xmlid -- only the
    // leaf "Tax Periods" item gets a step (see odoo-development-ui-test
    // skill, patterns-navigation-and-form.md §A).
    function openTaxPeriodMenuSteps() {
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
                content: "Open the Tax Periods menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_l10n_id_taxform.tax_period_menu"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list view --
                // the app landing action is also a .o_list_view.
                content: "Tax Periods list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Tax Periods)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/l10n_id_tax_period/01-create.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_l10n_id_taxform_l10n_id_tax_period_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTaxPeriodMenuSteps(), [
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
            // ── Flow 3 — Fill in Tax Period, Code, Tax Year, Date Start,
            // Date End. Tax Year (TOUR-TP-YEAR-UI) is the l10n_id.tax_year
            // fixture prepared in setUpClass -- Pre-Condition Data, not
            // the focus of this tour.
            {
                content: "Fill in Tax Period",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-TP-CREATE-UI",
            },
            {
                content: "Fill in Code",
                trigger: ".o_field_widget[name='code']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TP-CREATE-01",
            },
            {
                content: "Select the Tax Year",
                trigger: ".o_field_many2one[name='year_id'] input",
                run: "text TOUR-TP-YEAR-UI",
            },
            {
                content: "Pick the Tax Year from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR-TP-YEAR-UI)",
                in_modal: false,
            },
            {
                content: "Fill in Date Start",
                trigger: ".o_field_widget[name='date_start'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 01/01/2029",
            },
            {
                content: "Fill in Date End",
                trigger: ".o_field_widget[name='date_end'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 01/31/2029",
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
            // ── Post-Condition — a new tax period record is created,
            // active by default.
            {
                content: "Back to the Tax Periods list",
                trigger: ".breadcrumb-item.o_back_button a:contains(Tax Periods)",
            },
            {
                content: "New record appears in the list",
                trigger: ".o_data_row:contains(TOUR-TP-CREATE-UI)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );

    // ═══════════════════════════════════════════════════════════════
    // IK: docs/l10n_id_tax_period/02-edit.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_l10n_id_taxform_l10n_id_tax_period_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTaxPeriodMenuSteps(), [
            // ── Flow 2 — Find and open the record to edit.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-TP-EDIT-UI) .o_data_cell:first",
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
                run: "text_blur 02/05/2029",
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
    // IK: docs/l10n_id_tax_period/03-delete.md
    // ═══════════════════════════════════════════════════════════════
    tour.register(
        "ssi_l10n_id_taxform_l10n_id_tax_period_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openTaxPeriodMenuSteps(), [
            // ── Flow 2-4 — select the record and delete it, from the
            // record's own form. The 14.0 list-selector checkbox is
            // flaky (odoo-development-ui-test skill,
            // patterns-dialogs-and-wizards.md §I); opening the record
            // and deleting from its own Action menu reaches the same
            // Post-Condition.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-TP-DELETE-UI) .o_data_cell:first",
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
                content: "Back to the Tax Periods list",
                trigger: ".breadcrumb-item.o_back_button a:contains(Tax Periods)",
            },
            // ── Post-Condition — the record is permanently removed.
            {
                content: "Deleted tax period no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(" +
                    ".o_data_row:contains(TOUR-TP-DELETE-UI)))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );
});
