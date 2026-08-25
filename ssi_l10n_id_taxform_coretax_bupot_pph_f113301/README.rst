.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================================================================
Indonesia's Taxform - Coretax Bukti Potong PPh 21/26 f.1.1.33.01 Out XML Export
===============================================================================

This module extends the generic Coretax Bukti Potong PPh Out XML export
(``ssi_l10n_id_taxform_coretax_bupot_pph_out``) with the additional data the
DGT Coretax schema requires for BP21 (PPh 21/26 non-final withholding, form
f.1.1.33.01): PTKP status, tax facility, DPP, withholding rate, reference
document, and the recipient's ID TKU.


Configuration
=============

**Header**

1. Set *PTKP Category* and *Withholding Date* on the document before
   exporting.

**Lines**

1. Fill *Coretax Tax Object Code* (from the shared master) on each line; set
   its *Deemed* and *Tariff Type* on the master record.
2. Optionally set *Fasilitas Pajak* and the reference document fields.
3. *Rate Computation* is *Automatic* only when the tax object's *Tariff
   Type* is TER (looked up from the PPh 21 TER table using the header's PTKP
   category); every other tariff type must be entered as *Rate (Manual)*.


Usage
=====

1. Open an outgoing BP21 (f.1.1.33.01) record in the *Done* state.
2. Click the *Export Coretax XML* button in the form header.
3. The enriched XML file is downloaded automatically.


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/opnsynid-l10n-indonesia-taxform/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed
and welcomed feedback.

Credits
=======

Contributors
------------

* Andhitia Rama <andhitia.r@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
