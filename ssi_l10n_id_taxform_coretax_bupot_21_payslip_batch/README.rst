.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============================================================================
Indonesia's Taxform - Coretax PPh 21 Withholding XML from Payslip Batch
==============================================================================

This module adds the capability to generate the DJP Coretax BPMP XML file
(Bukti Pemotongan PPh 21 Pegawai Tetap - formulir 1721-VIII) directly from a
payslip batch. The generated XML follows the official Coretax bulk import schema
(``MmPayrollBulk``) and can be uploaded into the Coretax application.

The XML only contains employees who are actually subject to PPh 21 (the selected
withheld PPh 21 salary rule is greater than zero).


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/opnsynid-l10n-indonesia-taxform
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Indonesia's Taxform - Coretax PPh 21 Withholding XML from Payslip Batch*
6.  Install the module


Configuration
=============

**Withholder (Pemotong) Configuration**

The withholder identity is read from the batch company partner. Make sure to set:

1. *Tax ID (NPWP)* on the company partner (used as ``TIN``)
2. *NITKU* on the company partner (used as ``IDPlaceOfBusinessActivity`` / ID TKU)

**Employee Configuration**

For every employee subject to PPh 21, make sure the employee's private address
partner has:

1. *Tax ID (NPWP/NIK)* (used as ``CounterpartTin``)
2. *PTKP Category* (used as ``StatusTaxExemption``)

**PPh 21 TER Configuration**

The withholding ``Rate`` is taken from the PPh 21 TER (Tarif Efektif Rata-Rata)
table. Make sure the TER table is configured for the relevant period.


Usage
=====

To generate the Coretax XML, you need to:

1. Go to menu *Human Resources -> Payroll -> Payslip Batches*
2. Open a payslip batch in the *Done* state
3. Open the *Payslips* tab and click *Export Coretax PPh 21 XML*
4. Select the salary rule that holds the gross income (Penghasilan Bruto) and
   the salary rule that holds the withheld PPh 21
5. Click *Export* to download the XML file


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
* Michael Viriyananda <viriyananda.michael@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
