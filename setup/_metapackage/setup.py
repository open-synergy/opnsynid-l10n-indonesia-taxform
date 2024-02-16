import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-opnsynid-l10n-indonesia-taxform",
    description="Meta package for open-synergy-opnsynid-l10n-indonesia-taxform Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_l10n_id_taxform',
        'odoo14-addon-ssi_l10n_id_taxform_bukti_potong_pph_f113301',
        'odoo14-addon-ssi_l10n_id_taxform_bukti_potong_pph_f113301_work_log',
        'odoo14-addon-ssi_l10n_id_taxform_bukti_potong_pph_f113302',
        'odoo14-addon-ssi_l10n_id_taxform_bukti_potong_pph_f113302_work_log',
        'odoo14-addon-ssi_l10n_id_taxform_bukti_potong_pph_f113304',
        'odoo14-addon-ssi_l10n_id_taxform_bukti_potong_pph_f113306',
        'odoo14-addon-ssi_l10n_id_taxform_bukti_potong_pph_f113306_work_log',
        'odoo14-addon-ssi_l10n_id_taxform_bukti_potong_pph_f113308',
        'odoo14-addon-ssi_l10n_id_taxform_bukti_potong_pph_mixin',
        'odoo14-addon-ssi_l10n_id_taxform_faktur_pajak',
        'odoo14-addon-ssi_l10n_id_taxform_pph_21',
        'odoo14-addon-ssi_l10n_id_taxform_pph_21_payslip',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
