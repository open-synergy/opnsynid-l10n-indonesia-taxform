# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, models
from odoo.exceptions import Warning as UserError


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _check_taxform(self):
        self.ensure_one()
        self._cr.execute(
            """SELECT 1 FROM rel_bukpot_f113306_in_line_2_income_move
            WHERE account_move_id=%s
            """,
            (self.id,),
        )
        if self._cr.fetchone():
            return True
        else:
            return False

    def unlink(self):
        for move_line in self:
            taxform = move_line._check_taxform()
            if taxform:
                strWarning = _("You cannot delete journal item linked to taxform!")
                raise UserError(strWarning)
        return super(AccountMoveLine, self).unlink()
