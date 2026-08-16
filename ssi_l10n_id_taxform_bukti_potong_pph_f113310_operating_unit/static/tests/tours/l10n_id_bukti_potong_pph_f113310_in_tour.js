/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

odoo.define(
    "ssi_l10n_id_taxform_bukti_potong_pph_f113310_operating_unit." +
        "l10n_id_bukti_potong_pph_f113310_in_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/l10n_id_bukti_potong_pph_f113310_in/01-create.md
        // (E1 delta -- Additional Fields). Navigation (open menu ->
        // New) is taken from the base IK
        // ssi_l10n_id_taxform_bukti_potong_pph_f113310/docs/
        // l10n_id_bukti_potong_pph_f113310_in/01-create.md Flow steps
        // 1-2 -- see skill odoo-development-ui-test,
        // scope-and-boundaries.md §1 ("Backing dua file: tour
        // extension = base IK ∪ delta IK"). The delta assertion comes
        // from this module's own IK: the Operating Unit field is
        // visible on the create form for a user in the
        // operating_unit.group_multi_operating_unit group. The tour
        // stops there; it does not fill, save, or confirm (E1
        // delta-only).
        tour.register(
            "ssi_l10n_id_taxform_bukti_potong_pph_f113310_operating_unit_" +
                "l10n_id_bukti_potong_pph_f113310_in_create",
            {test: true, url: "/web"},
            [
                // ── Base Flow 1 — Open the Taxform > Bukti Potong >
                // PPh 4(2) (f.1.1.33.10) In menu.
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
                    content: "Open the PPh 4(2) (f.1.1.33.10) In menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_l10n_id_taxform_bukti_potong_pph_f113310.bukti_potong_pph_42_in_menu"]',
                },
                {
                    // NOTE: this menu's label contains literal
                    // parentheses, which jQuery's `:contains()`
                    // selector cannot match reliably. Match the
                    // parenthesis-free form number instead.
                    content: "PPh 4(2) (f.1.1.33.10) In list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(f.1.1.33.10)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },

                // ── Base Flow 2 — Click the New button. (14.0: "Create")
                {
                    content: "Click Create",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },

                // ── Delta assertion — the Operating Unit field is
                // visible on the create form for a user in the multi
                // operating unit group. The tour stops here (E1
                // delta-only).
                {
                    content: "Operating Unit field is visible on the form",
                    trigger:
                        ".o_form_view.o_form_editable .o_field_widget[name='operating_unit_id']",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ]
        );
    }
);
