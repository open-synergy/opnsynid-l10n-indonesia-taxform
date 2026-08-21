# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import base64
import hashlib
import hmac
import time
from datetime import datetime
from wsgiref.handlers import format_date_time

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class KlikpajakBackend(models.Model):
    """
    Represent one Klikpajak API backend configuration per company.

    Holds the base URL, authentication credentials (JWT/Basic/HMAC),
    the outbound e-Faktur endpoints, and a free-form list of extra API
    parameters (``parameter_value_ids``). Only one backend per company
    can be ``running`` at a time — ``action_running`` enforces this by
    demoting any other running backend of the same company back to
    ``draft`` and links the chosen backend to
    ``res.company.klikpajak_backend_id``.
    """

    _name = "klikpajak_backend"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Klik Pajak Backend"
    _automatically_insert_print_button = False

    @api.model
    def _default_company_id(self):
        """Return the current user's company as the default company.

        :return: ``id`` of ``self.env.user.company_id``.
        """
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
        copy=True,
    )
    auth_method = fields.Selection(
        string="Authentication",
        selection=[
            ("jwt", "JWT (JSON Web Token)"),
            ("basic", "Basic Authentication"),
            ("hmac", "HMAC (Hash-based Message Authentication Code)"),
        ],
        copy=False,
        default="hmac",
        required=True,
        readonly=False,
    )
    parameter_value_ids = fields.One2many(
        string="API Parameters",
        comodel_name="klikpajak_backend.parameter",
        inverse_name="backend_id",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("running", "Running"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )

    # GENERAL
    base_url = fields.Char(
        string="Base URL",
        required=True,
        copy=True,
    )
    exclude_product_ids = fields.Many2many(
        string="Exclude Products",
        comodel_name="product.product",
        relation="rel_company_2_klikpajak_product",
        column1="company_id",
        column2="product_id",
    )
    # API
    sale_invoice_api = fields.Char(
        string="Create Sale Invoice",
        required=True,
        copy=True,
        default="/v2/klikpajak/v2/efaktur/out",
    )
    cancel_sale_invoice_api = fields.Char(
        string="Cancel Sale Invoice",
        required=True,
        copy=True,
        default="/v2/klikpajak/v2/efaktur/out/{id}/cancel/",
    )
    approve_sale_invoice_api = fields.Char(
        string="Approve Sale Invoice",
        required=True,
        copy=True,
        default="/v2/klikpajak/v2/efaktur/out/{id}/approve/",
    )
    retrieve_sale_invoice_api = fields.Char(
        string="Retrieve Sale Invoice",
        required=True,
        copy=True,
        default="/v2/klikpajak/v2/efaktur/out/{id}",
    )
    # BUAT AUTH JWT
    token = fields.Char(
        string="Token",
        copy=False,
    )
    # BUAT AUTH BASIC
    username = fields.Char(
        string="Username",
        copy=False,
    )
    password = fields.Char(
        string="Password",
        copy=False,
    )
    # BUAT AUTH BASIC USE PYTHON
    client_id = fields.Char(
        string="Client ID",
        copy=False,
    )
    client_secret = fields.Char(
        string="Client Secret",
        copy=False,
    )

    def _get_klikpajak_date_header(self):
        """Build the ``Date`` header value for a Klikpajak request.

        Formats the current UTC time as an HTTP-date string (RFC
        1123, e.g. ``Mon, 21 Aug 2026 09:00:00 GMT``) via
        ``wsgiref.handlers.format_date_time``. Klikpajak signs
        requests over UTC-formatted date strings, so this is the
        value that is expected to also appear in the ``date:`` line
        signed by :meth:`_get_signature`.

        :return: HTTP-date formatted UTC timestamp string.
        """
        self.ensure_one()
        now_timestamp = time.mktime(datetime.utcnow().timetuple())
        return format_date_time(now_timestamp)

    def _get_klikpajak_sale_invoice_params(self):
        """Build the query parameters for the Create Sale Invoice call.

        Used when calling ``sale_invoice_api`` (the e-Faktur "create
        sale invoice" endpoint): asks Klikpajak to auto-approve and
        auto-calculate the submitted invoice, so no separate approve
        call is required for backends configured this way.

        :return: dict with ``auto_approval`` and ``auto_calculate``,
            both set to the string ``"true"``.
        """
        self.ensure_one()
        return {
            "auto_approval": "true",
            "auto_calculate": "true",
        }

    def _get_klikpajak_header(self):
        """Build the base HTTP headers shared by every Klikpajak call.

        Currently only the ``Date`` header (see
        :meth:`_get_klikpajak_date_header`). :meth:`_get_header`
        extends this dict with ``Authorization`` before a request is
        sent.

        :return: dict with the ``Date`` header.
        """
        self.ensure_one()
        return {
            "Date": self._get_klikpajak_date_header(),
        }

    def _get_klikpajak_authorization_header(self, signature):
        """Build the ``Authorization`` header for HMAC authentication.

        Composes the ``hmac`` authentication scheme Klikpajak expects:
        ``username`` set to ``client_id``, fixed
        ``algorithm="hmac-sha256"``, ``headers="date request-line"``
        (naming the two signed lines), and the given ``signature``.

        :param str signature: base64-encoded HMAC-SHA256 signature,
            as returned by :meth:`_get_signature`.
        :return: the fully formatted ``Authorization`` header value.
        """
        self.ensure_one()
        result = 'hmac username="%s",' % self.client_id
        result += ' algorithm="hmac-sha256",'
        result += ' headers="date request-line",'
        result += ' signature="%s"' % (signature)
        return result

    def _get_signature(self, date, path, method):
        """Compute the HMAC-SHA256 signature of one API request.

        Signs the two-line payload ``"date: <date>\\n<method> <path>
        HTTP/1.1"`` using ``client_secret`` as the HMAC key, then
        base64-encodes the resulting digest. This is the ``date`` +
        request-line pair the ``Authorization`` header (see
        :meth:`_get_klikpajak_authorization_header`) declares as
        signed via ``headers="date request-line"``.

        :param str date: HTTP-date string to sign, normally the
            value returned by :meth:`_get_klikpajak_date_header`.
        :param str path: request path (or full URL — see
            :meth:`_get_hmac`) to sign as part of the request line.
        :param str method: HTTP method to sign, upper case (e.g.
            ``"POST"``).
        :return: base64-encoded HMAC-SHA256 signature string.
        """
        secret = self.client_secret
        request_line = method + " " + path + " HTTP/1.1"
        payload_tupple = ("date: " + date, request_line)
        payload = "\n".join(payload_tupple)

        hmac1 = hmac.new(
            key=secret.encode("utf-8"),
            msg=payload.encode("utf-8"),
            digestmod=hashlib.sha256,
        )
        message_digest1 = hmac1.digest()

        signature = base64.b64encode(message_digest1).decode("utf-8")
        return signature

    def _get_header(self, path, method):
        """Build the full HTTP headers for one signed Klikpajak call.

        Combines :meth:`_get_klikpajak_header` (which carries a UTC
        ``Date``) with a freshly computed ``Authorization`` header:
        ``path``/``method`` are signed with the *local* current
        timestamp via :meth:`_get_signature` and
        :meth:`_get_klikpajak_authorization_header` — a separate
        timestamp from the one already in the ``Date`` header above.

        :param str path: request path being called and signed.
        :param str method: HTTP method of the request, upper case
            (e.g. ``"POST"``).
        :return: dict of headers, including ``Date`` and
            ``Authorization``.
        """
        self.ensure_one()
        result = self._get_klikpajak_header()
        date = format_date_time(datetime.now().timestamp())
        signature = self._get_signature(date, path, method)
        authorization = self._get_klikpajak_authorization_header(signature)
        result.update(
            {
                "Authorization": authorization,
            }
        )
        return result

    def _get_hmac(self):
        """Compute the HMAC signature for the Create Sale Invoice call.

        Signs ``base_url`` + ``sale_invoice_api`` as a ``POST``
        request, using the current local timestamp (see
        :meth:`_get_signature`). Used by :meth:`action_get_hmac` to
        let a user verify the configured ``client_id``/
        ``client_secret`` pair produces a signature, without sending
        an actual request to Klikpajak.

        :return: base64-encoded HMAC-SHA256 signature string.
        """
        self.ensure_one()
        date = format_date_time(datetime.now().timestamp())
        api_url = self.base_url + self.sale_invoice_api
        result = self._get_signature(date, api_url, "POST")
        return result

    def action_get_hmac(self):
        """Show the computed HMAC signature to the user.

        For every record in ``self``, computes the signature via
        :meth:`_get_hmac` and raises a ``ValidationError`` carrying
        the result — this dialog is the only way the value is
        surfaced, since :meth:`_get_hmac` is never stored on a field.
        Intended as a manual check that the configured ``client_id``/
        ``client_secret`` pair signs correctly; it does not call the
        Klikpajak API and does not change ``state``.

        :raises ValidationError: always, carrying the computed
            signature as its message — this is the expected way the
            action reports its result, not a failure.
        """
        for record in self:
            result = record._get_hmac()
            raise ValidationError(  # pylint: disable=translation-required
                f"Result: {result}"
            )

    def action_running(self):
        """Set the backend as the running backend of its company.

        **Side effect:** any other backend of the same company that is
        currently ``running`` is demoted back to ``draft`` first, since
        only one backend per company can be running at a time. The
        record is then linked to
        ``res.company.klikpajak_backend_id`` and its own ``state`` is
        set to ``running``.
        """
        for record in self:
            check_running_backend_ids = self.search(
                [
                    ("state", "=", "running"),
                    ("company_id", "=", self.env.user.company_id.id),
                    ("id", "!=", record.id),
                ]
            )
            if check_running_backend_ids:
                check_running_backend_ids.write({"state": "draft"})
            record.company_id.write({"klikpajak_backend_id": record.id})
            record.write({"state": "running"})

    def action_restart(self):
        """Return the backend to ``draft`` and unlink it from its company.

        Clears ``res.company.klikpajak_backend_id`` when it points to
        this record, then sets ``state`` back to ``draft``.
        """
        for record in self:
            record.company_id.write({"klikpajak_backend_id": False})
            record.write({"state": "draft"})
