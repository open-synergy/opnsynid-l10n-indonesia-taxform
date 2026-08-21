// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_l10n_id_taxform.res_partner_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/res_partner/01-create.md (E1 delta -- Additional Fields)
    // There is no base Instruksi Kerja for res.partner (Odoo core), so
    // navigation is taken straight from Odoo's own Contacts app: the
    // "Contacts" item (contacts.res_partner_menu_contacts) is the only
    // content menu under the Contacts app root (contacts.menu_contacts)
    // besides admin-only "Configuration", so opening the app already
    // lands on it -- no separate menu click is needed.
    tour.register(
        "ssi_l10n_id_taxform_res_partner_create",
        {
            test: true,
            url: "/web",
        },
        [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Contacts app",
                trigger: '.o_app[data-menu-xmlid="contacts.menu_contacts"]',
            },
            {
                content: "Contacts kanban is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Contacts)",
                extra_trigger: ".o_kanban_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // ── Click New. (14.0: "Create")
            {
                content: "Click New",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_kanban_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // ── Delta assertion -- the NITKU field is visible on the
            // create form and can be filled in. The tour stops here
            // without saving (E1 delta-only); saved/persisted value is
            // out of scope for a tour.
            {
                content: "Fill in NITKU",
                // Char field root element IS the <input> at 14.0
                // (InputField.init sets tagName='input') -- "... input"
                // would search for an input inside an input and time out.
                trigger: ".o_field_widget[name='nitku']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 12.345.678.9-012.000",
            },
        ]
    );
});
