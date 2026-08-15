# Create Tax Form 1721 A1

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_1721_a1`\
> **Model:** `l10n_id.bukti_potong_pph_1721_a1`\
> **Menu:** Taxform > Bukti Potong > Tax Form 1721 A1\
> **Actor:** user in group `Bukti Potong PPh 21 1721 A1 / User`\
> **State:** `—` → `draft`

## Pre-Condition

- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group (needed before the record can later be confirmed).
- **Config:** An active `approval.template` for this model exists (needed for the later
  Confirm/Approve flow).
- **Data:** The **Wajib Pajak** (taxpayer, `res.partner`, an individual with no parent
  company) already exists, with NIK, NPWP, address, PTKP category, and job position
  filled in on the partner record.
- **Data:** The **Pemotong Pajak** (withholding party, `res.partner`, a company) already
  exists.
- **Data:** The **Kode Objek Pajak**, **Period Awal**, and **Period Akhir** master data
  already exist.
- **Access:** User is in group `Bukti Potong PPh 21 1721 A1 / User`.

## Flow

1. Open the **Taxform > Bukti Potong > Tax Form 1721 A1** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Company** _(required)_: Automatically filled from the current user's company.
     Change if needed.
   - **Wajib Pajak** _(required)_: Select the taxpayer. Automatically fills **NPWP**,
     **NIK**, **Alamat**, **Alamat2**, **ZIP**, **Kota**, **State**, **Negara**, **PTKP
     Kategori**, and **Jabatan** from the selected partner. Change if needed.
   - **Kode Objek Pajak** _(required)_: Select the applicable tax object code.
   - **Pemotong Pajak** _(required)_: Automatically filled from the current company's
     partner. Change if needed.
   - **Date** _(required)_: Automatically filled with today's date. Change if needed.
   - **Period Awal** _(required)_: Select the starting tax period.
   - **Period Akhir** _(required)_: Select the ending tax period.
4. On the **Informasi Umum** tab, review the fields auto-filled from **Wajib Pajak** in
   step 3 (**Alamat**, **Kota**, **State**, **Negara**, **ZIP**, **Jabatan**, etc.).
   Fill in **Karyawan Asing** and **Kode Negara Domisili** if relevant.
5. On the **Penghasilan Bruto** tab, fill in the gross income components (**GAJI/PENSIUN
   ATAU THT/JHT**, **TUNJANGAN PPh**, and so on). Each field is automatically filled
   from the company's Form 1721 A1 configuration (see `res.company` > **Form 1721 A1**
   tab) whenever **Company**, **Wajib Pajak**, **Period Awal**, or **Period Akhir**
   changes. Change if needed. **JUMLAH PENGHASILAN BRUTO** is computed automatically
   from these fields.
6. On the **Pengurangan** tab, review **BIAYA JABATAN/BIAYA PENSIUN** (computed) and
   fill in **IURAN PENSIUN ATAU IURAN THT/JHT** if not already auto-filled from company
   configuration. **JUMLAH PENGURANGAN** is computed automatically.
7. On the **Penghitungan PPh Pasal 21** tab, review the computed fields (**JUMLAH
   PENGHASILAN NETO**, **PENGHASILAN TIDAK KENA PAJAK (PTKP)**, **PENGHASILAN KENA
   PAJAK**, **PPh PASAL 21 ATAS PENGHASILAN KENA PAJAK**, **PPh PASAL 21 TERUTANG**) and
   fill in **PENGHASILAN NETO MASA SEBELUMNYA**, **PPh PASAL 21 YANG TELAH DIPOTONG MASA
   SEBELUMNYA**, and **PPh PASAL 21 DAN PPh PASAL 26 YANG TELAH DIPOTONG DAN DILUNASI**
   if not already auto-filled from company configuration.
8. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status. **(14.0: Save keeps the form open in
  read-only mode; it does not navigate back to the list.)**
- The document number stays **/** until the record is confirmed and approved.
