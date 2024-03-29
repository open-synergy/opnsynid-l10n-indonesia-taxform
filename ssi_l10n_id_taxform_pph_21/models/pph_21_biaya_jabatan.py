# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class Pph21TunjanganJabatan(models.Model):
    _name = "l10n_id.pph_21_biaya_jabatan"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Biaya Jabatan"
    _order = "date_start desc, id"

    date_start = fields.Date(
        string="Tanggal Mulai Berlaku",
        required=True,
    )
    rate_biaya_jabatan = fields.Float(
        string="Rate Biaya Jabatan",
        required=True,
    )
    max_biaya_jabatan = fields.Float(
        string="Max. Biaya Jabatan",
        required=True,
    )

    _sql_constraints = [
        ("date_start_unique", "unique(date_start)", _("Date start has to be unique"))
    ]

    @api.model
    def find(self, dt=None):
        if not dt:
            dt = datetime.now().strftime("%Y-%m-%d")
        criteria = [("date_start", "<=", dt)]
        results = self.search(criteria, limit=1)
        if not results:
            strWarning = _("No biaya jabatan configuration for %s" % dt)
            raise ValidationError(strWarning)
        return results[0]

    def get_biaya_jabatan_rutin(self, jumlah_penghasilan_rutin=0.0, is_keluar=False):
        self.ensure_one()
        multiply = (self.rate_biaya_jabatan / 100.00) * jumlah_penghasilan_rutin
        maximum_jabatan = self.max_biaya_jabatan
        if is_keluar:
            maximum_jabatan = 12 * self.max_biaya_jabatan
        if multiply >= maximum_jabatan:
            result = maximum_jabatan
        else:
            result = multiply

        return result

    def get_biaya_jabatan_non_rutin(
        self, jumlah_penghasilan_non_rutin=0.0, biaya_jabatan_rutin=0.0, is_keluar=False
    ):
        self.ensure_one()
        multiply = (self.rate_biaya_jabatan / 100.0) * jumlah_penghasilan_non_rutin
        maximum_jabatan = self.max_biaya_jabatan
        if is_keluar:
            maximum_jabatan = 12 * self.max_biaya_jabatan
        if multiply + biaya_jabatan_rutin >= maximum_jabatan:
            result = maximum_jabatan - biaya_jabatan_rutin
        else:
            result = multiply
        return result

    def get_biaya_jabatan(
        self,
        jumlah_penghasilan_rutin=0.0,
        jumlah_penghasilan_rutin_setahun=0.0,
        jumlah_penghasilan_non_rutin=0.0,
        is_keluar=False,
    ):
        # TODO:
        self.ensure_one()
        result = {
            "biaya_jabatan_rutin_setahun": 0.0,
            "biaya_jabatan_non_rutin_setahun": 0.0,
            "biaya_jabatan_setahun": 0.0,
            "biaya_jabatan": 0.0,
        }
        if not is_keluar:
            biaya_jabatan_rutin = self.get_biaya_jabatan_rutin(
                jumlah_penghasilan_rutin, is_keluar
            )
            biaya_jabatan_non_rutin = self.get_biaya_jabatan_non_rutin(
                jumlah_penghasilan_non_rutin, biaya_jabatan_rutin, is_keluar
            )
            biaya_jabatan = biaya_jabatan_rutin + biaya_jabatan_non_rutin
            biaya_jabatan_rutin_setahun = self.get_biaya_jabatan_rutin(
                jumlah_penghasilan_rutin_setahun, True
            )
            biaya_jabatan_non_rutin_setahun = self.get_biaya_jabatan_non_rutin(
                jumlah_penghasilan_non_rutin, biaya_jabatan_rutin_setahun, True
            )
            biaya_jabatan_setahun = (
                biaya_jabatan_rutin_setahun + biaya_jabatan_non_rutin_setahun
            )
        else:
            biaya_jabatan_rutin_setahun = self.get_biaya_jabatan_rutin(
                jumlah_penghasilan_rutin_setahun, True
            )
            biaya_jabatan_non_rutin_setahun = self.get_biaya_jabatan_non_rutin(
                jumlah_penghasilan_non_rutin, biaya_jabatan_rutin_setahun, True
            )
            biaya_jabatan = (
                biaya_jabatan_rutin_setahun + biaya_jabatan_non_rutin_setahun
            )
            biaya_jabatan_setahun = (
                biaya_jabatan_rutin_setahun + biaya_jabatan_non_rutin_setahun
            )

        result["biaya_jabatan_rutin_setahun"] = biaya_jabatan_rutin_setahun
        result["biaya_jabatan_non_rutin_setahun"] = biaya_jabatan_non_rutin_setahun
        result["biaya_jabatan_setahun"] = biaya_jabatan_setahun
        result["biaya_jabatan"] = biaya_jabatan

        return result
