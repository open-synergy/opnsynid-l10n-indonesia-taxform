# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import json
from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class KlikpajakBackendParameter(models.Model):
    """
    Store one API parameter of a Klikpajak backend record.

    This is a detail/child model: each row belongs to exactly one
    ``klikpajak_backend`` (see ``backend_id``) and its rows are edited
    inline from the parent's ``parameter_value_ids`` field. Values are
    kept as plain text (``value``) and typed/parsed on demand through
    ``parse_value``, so a single free-text column can hold string,
    number, boolean, JSON, date, or datetime data depending on
    ``type``.
    """

    _name = "klikpajak_backend.parameter"
    _description = "Klikpajak Backend Parameter Definition"

    backend_id = fields.Many2one(
        string="#Backend ID",
        comodel_name="klikpajak_backend",
        required=True,
        ondelete="cascade",
    )
    name = fields.Char(
        string="Parameter Name",
        required=True,
        help="Name of the parameter."
        "This is used to identify the parameter in the script.",
    )
    type = fields.Selection(
        string="Parameter Type",
        selection=[
            ("char", "String"),
            ("int", "Integer"),
            ("float", "Float"),
            ("bool", "Boolean"),
            ("json", "JSON Object"),
            ("date", "Date"),
            ("datetime", "Datetime"),
        ],
        default="char",
        required=True,
        help="Type of the parameter."
        "This determines how the parameter is processed in the script.",
    )
    description = fields.Text(
        string="Description",
        help="Detailed description of the parameter."
        "This is used to provide additional context or usage information.",
    )
    value = fields.Char(string="Value", help="Value for the parameter.")

    @api.constrains(
        "value",
        "type",
    )
    def _check_value_format(self):
        """Validate that ``value`` parses under the selected ``type``.

        Runs ``int``/``float``/JSON/date/datetime parsing (or checks
        the ``bool`` literal set) against ``value`` for each record;
        any parsing failure means the stored text cannot be trusted
        by ``parse_value`` later, so it must be rejected here instead.

        :raises ValidationError: when ``value`` cannot be parsed as
            ``type`` for one of the records in ``self``.
        """
        for record in self:
            t = record.type
            v = record.value
            try:
                if t == "int":
                    int(v)
                elif t == "float":
                    float(v)
                elif t == "bool":
                    if v.lower() not in ("1", "0", "true", "false", "yes", "no"):
                        raise ValueError()
                elif t == "json":
                    json.loads(v)
                elif t == "date":
                    datetime.strptime(v, "%Y-%m-%d")
                elif t == "datetime":
                    datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            except Exception:
                raise ValidationError(  # pylint: disable=translation-required
                    f"Invalid value format for parameter '{record.name}' (type {t})."
                )

    def parse_value(self):
        """Convert the stored text ``value`` to its typed Python value.

        Called by code that consumes a parameter row and needs the
        actual ``int``/``float``/``bool``/``dict``/``date``/
        ``datetime`` instead of the raw text stored in ``value``.
        Falls back to returning ``value`` unchanged for ``type ==
        "char"``.

        :return: the parsed value, typed according to ``type``.
        :raises UserError: when ``value`` cannot be parsed as
            ``type`` — this can only happen if
            ``_check_value_format`` was bypassed (e.g. import).
        """
        t = self.type
        v = self.value
        try:
            if t == "int":
                return int(v)
            elif t == "float":
                return float(v)
            elif t == "bool":
                return v.lower() in ("1", "true", "yes")
            elif t == "json":
                return json.loads(v)
            elif t == "date":
                return datetime.strptime(v, "%Y-%m-%d").date()
            elif t == "datetime":
                return datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            return v
        except Exception as e:
            raise UserError(  # pylint: disable=translation-required
                f"Invalid value for parameter '{self.name}': {e}"
            )
