/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

odoo.define(
    "ssi_l10n_id_taxform_bukti_potong_pph_f113308_operating_unit" +
        ".l10n_id_bukti_potong_pph_f113308_out_operating_unit_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // ── IK: docs/l10n_id_bukti_potong_pph_f113308_out/01-create.md
        // (E1 delta -- Additional Fields). Navigation (open menu -> New)
        // is taken from the base IK
        // ssi_l10n_id_taxform_bukti_potong_pph_f113308/docs/
        // l10n_id_bukti_potong_pph_f113308_out/01-create.md Flow steps
        // 1-2 -- see scope-and-boundaries.md skill
        // odoo-development-ui-test §1 ("Backing dua-file: tour
        // extension = base IK ∪ delta IK"). The delta assertions come
        // from this module's own IK: the Operating Unit field is
        // visible AND editable on the create form for a user in the
        // operating_unit.group_multi_operating_unit group. The tour
        // stops there; it does not fill, save or confirm (E1
        // delta-only).
        tour.register(
            "ssi_l10n_id_taxform_bukti_potong_pph_f113308_operating_unit" +
                "_l10n_id_bukti_potong_pph_f113308_out_create",
            {test: true, url: "/web"},
            [
                // ── Base Flow 1 — Open the Taxform > Bukti Potong >
                // PPh 26 (f.1.1.33.08) Out menu.
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
                    content: "Open the PPh 26 (f.1.1.33.08) Out menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_l10n_id_taxform_bukti_potong_pph_f113308.bukti_potong_pph_26_out_menu"]',
                },
                {
                    content: "PPh 26 (f.1.1.33.08) Out list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(PPh 26)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // ── Base Flow 2 — Click the New button.
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

                // ── Delta assertion 1 — the Operating Unit field is
                // visible on the create form for a user in the multi
                // operating unit group.
                {
                    content: "Operating Unit field is visible on the form",
                    trigger:
                        ".o_form_view.o_form_editable .o_field_widget[name='operating_unit_id']",
                    run: function () {
                        // Assertion only.
                    },
                },

                // ── Delta assertion 2 — the field is editable. An
                // editable many2one renders an <input> inside a
                // `.o_field_many2one` wrapper (FieldMany2One template,
                // web/static/src/xml/base.xml); the readonly rendering
                // (`.o_form_uri` link or plain `<span>`) has neither the
                // class nor the input.
                {
                    content: "Operating Unit field is editable",
                    trigger:
                        ".o_form_view.o_form_editable .o_field_many2one[name='operating_unit_id'] input",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );
    }
);
