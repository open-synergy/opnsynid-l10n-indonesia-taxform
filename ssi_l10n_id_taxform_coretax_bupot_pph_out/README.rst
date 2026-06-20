.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============================================================================
Indonesia's Taxform - Coretax Bukti Potong PPh Out XML Export
==============================================================================

This module adds the capability to generate a DJP Coretax XML file directly
from any outgoing Bukti Potong PPh record (direction = "out"). The generated
XML file (``MmBulkWithholding``) can be uploaded into the Coretax application.

One ``MmWithholding`` element is produced for each line in the bukti potong
whose withheld tax amount (``amount_tax``) is greater than zero.


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/opnsynid-l10n-indonesia-taxform
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Indonesia's Taxform - Coretax Bukti Potong PPh Out XML Export*
6.  Install the module


Configuration
=============

**Withholder (Pemotong) Configuration**

The withholder identity is read from ``pemotong_pajak_id``. Make sure to set:

1. *Tax ID (NPWP)* on the partner (used as ``TIN``)
2. *NITKU* on the partner (used as ``IDPlaceOfBusinessActivity`` / ID TKU)

**Wajib Pajak Configuration**

For every wajib pajak, make sure the partner has:

1. *Tax ID (NPWP)* (used as ``CounterpartTin``)
2. *Country* (used to determine ``CounterpartOpt``: Resident or NonResident)

**Coretax Tax Object Code**

Each bukti potong PPh line has a *Coretax Tax Object Code* field. Fill this
with the appropriate DJP tax object code (e.g. ``23-100-01`` for PPh 23
on interest income) before exporting.


Usage
=====

1. Open any outgoing Bukti Potong PPh record in the *Done* state
2. Fill the *Coretax Tax Object Code* on each line
3. Click the *Export Coretax XML* button in the form header
4. The XML file will be downloaded automatically


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
