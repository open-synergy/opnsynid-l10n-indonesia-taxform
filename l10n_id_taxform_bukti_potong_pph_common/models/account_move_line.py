# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, _
from openerp.exceptions import Warning as UserError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.multi
    def _check_taxform(self):
        self.ensure_one()
        self._cr.execute(
            """SELECT 1 FROM rel_bukpot_line_2_income_move
            WHERE account_move_id=%s
            """,
            (self.id,))
        if self._cr.fetchone():
            return True
        else:
            return False

    @api.multi
    def unlink(self):
        for move_line in self:
            taxform = move_line._check_taxform()
            if taxform:
                raise UserError(
                    _("Warning!"),
                    _("You cannot delete journal item linked to taxform!")
                )
        return super(AccountMoveLine, self).unlink()
