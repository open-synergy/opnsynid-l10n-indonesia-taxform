# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Indonesia - Form Bukti Potong 1721 A1",
    "version": "8.0.1.1.0",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "l10n_id_taxform_period",
        "l10n_id_taxform_pph_21",
        "l10n_id_taxform_objek_pajak",
        "l10n_id_partner_identification_kependudukan",
        "partner_contact_gender",
        "base_sequence_configurator",
        "base_workflow_policy",
        "base_print_policy",
        "base_multiple_approval",
        "base_cancel_reason",
        "base_custom_information",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_module_category_data.xml",
        "security/res_groups_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "data/base_sequence_configurator_data.xml",
        "views/bukti_potong_1721_a1_views.xml",
        "views/res_company_views.xml",
        "views/taxform_1721a1_config_setting_views.xml",
    ],
}
