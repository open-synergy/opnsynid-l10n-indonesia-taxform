/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

odoo.define(
    "ssi_l10n_id_taxform_coretax_bupot_pph_f113301." +
        "l10n_id_bukti_potong_pph_f113301_out_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // ── Menu: Taxform > Bukti Potong > PPh 21/26 Tidak Final
        // (f.1.1.33.01) Out (Flow step 1 of the IK in this file). Same
        // menu path as the base module's tour — the menu itself is
        // provided by ``ssi_l10n_id_taxform_bukti_potong_pph_f113301``.
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
                content: "Open the PPh 21/26 Tidak Final (f.1.1.33.01) Out menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_l10n_id_taxform_bukti_potong_pph_f113301.bukti_potong_pph_2126_out_menu"]',
            },
            {
                content: "PPh 21/26 Tidak Final (f.1.1.33.01) Out list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(PPh 21/26 Tidak Final)",
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

        // ── IK: docs/l10n_id_bukti_potong_pph_f113301_out/
        // 07-input-nomor-coretax.md
        tour.register(
            "ssi_l10n_id_taxform_coretax_bupot_pph_f113301_" +
                "l10n_id_bukti_potong_pph_f113301_out_input_nomor_coretax",
            {test: true, url: "/web"},
            [].concat(
                openMenuSteps,
                // ── Flow 2 — Open the record that is Waiting for
                // Approval.
                openRecordSteps("TOUR WP InputNomorCoretaxF113301"),
                [
                    {
                        content: "Status is Waiting for Approval",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    // ── Flow 3 — Click Edit.
                    {
                        content: "Click Edit",
                        trigger: ".o_form_button_edit",
                        extra_trigger: ".o_form_view.o_form_readonly",
                    },
                    // ── Flow 4 — Type the Coretax number into the
                    // Number field.
                    {
                        content: "Type the Coretax number into the Number field",
                        trigger: ".oe_title .o_field_widget[name='name']",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text BP-CORETAX-0001",
                    },
                    // ── Flow 5 — Click Save.
                    {
                        content: "Save the record",
                        trigger: ".o_form_button_save",
                    },
                ],
                // ── Post-Condition — the Number shows the typed value.
                [
                    {
                        content: "Number shows the Coretax number",
                        trigger:
                            ".o_form_readonly .oe_title .o_field_widget[name='display_name']:contains(BP-CORETAX-0001)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );
    }
);
