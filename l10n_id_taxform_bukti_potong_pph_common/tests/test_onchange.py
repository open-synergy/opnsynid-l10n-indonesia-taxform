# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from .base import BaseCase


class TestOnchange(BaseCase):
    def test_bukti_potong_pph_onchange_period_id(self):
        date = datetime.now().strftime("%Y-%m-%d")
        values = {
            "date": date,
        }
        bukti_potong_pph = self.obj_bukti_potong_pph.new(values)
        bukti_potong_pph.onchange_period_id()
        period_id = self.obj_period.find(date).id
        self.assertEqual(bukti_potong_pph.period_id.id, period_id)

    def test_bukti_potong_pph_onchange_pemotong_pajak_id(self):
        values = {
            "pemotong_pajak_id": False,
        }
        bukti_potong_pph = self.obj_bukti_potong_pph.new(values)
        bukti_potong_pph.onchange_pemotong_pajak_id()
        self.assertFalse(bukti_potong_pph.ttd_id)
