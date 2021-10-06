# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class BaseCase(TransactionCase):
    def setUp(self, *args, **kwargs):
        result = super(BaseCase, self).setUp(*args, **kwargs)
        self.obj_bukti_potong_pph = self.env["l10n_id.bukti_potong_pph"]
        self.obj_period = self.env["account.period"]
        return result
