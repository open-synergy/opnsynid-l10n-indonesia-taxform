import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-open-synergy-opnsynid-l10n-indonesia-taxform",
    description="Meta package for open-synergy-opnsynid-l10n-indonesia-taxform Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-l10n_id_taxform',
        'odoo11-addon-l10n_id_taxform_faktur_pajak_common',
        'odoo11-addon-ssi_l10n_id_taxform_bukti_potong_pph_f113306',
        'odoo11-addon-ssi_l10n_id_taxform_bukti_potong_pph_mixin',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 11.0',
    ]
)
