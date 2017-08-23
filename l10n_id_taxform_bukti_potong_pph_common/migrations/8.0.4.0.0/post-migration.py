# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID
from openerp.api import Environment


def migrate(cr, version):
    if not version:
        return

    env = Environment(cr, SUPERUSER_ID, {})
    obj_bukti_potong_line =\
        env['l10n_id.bukti_potong_pph_line']
    line_ids =\
        obj_bukti_potong_line.search([('name', '=', '/')])
    for line in line_ids:
        tax_code_name = line.tax_code_id.name
        cr.execute('UPDATE l10n_id_bukti_potong_pph_line '
                   'SET name = \'%s\' '
                   'WHERE id = %d;' %
                   (tax_code_name, line))
