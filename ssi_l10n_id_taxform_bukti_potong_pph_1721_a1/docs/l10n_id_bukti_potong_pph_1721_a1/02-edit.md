# Edit Tax Form 1721 A1

> **Module:** `ssi_l10n_id_taxform_bukti_potong_pph_1721_a1`\
> **Model:** `l10n_id.bukti_potong_pph_1721_a1`\
> **Menu:** Taxform > Bukti Potong > Tax Form 1721 A1\
> **Actor:** user in group `Bukti Potong PPh 21 1721 A1 / User`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group `Bukti Potong PPh 21 1721 A1 / User`.

## Flow

1. Open the **Taxform > Bukti Potong > Tax Form 1721 A1** menu.
2. Find and open the record to edit.
3. Change the required fields (**Wajib Pajak**, **Kode Objek Pajak**, **Pemotong
   Pajak**, **Date**, **Period Awal**, **Period Akhir**) or any income/deduction field
   on the **Penghasilan Bruto**, **Pengurangan**, or **Penghitungan PPh Pasal 21** tabs.
4. Changing **Wajib Pajak** re-fills the identity fields on the **Informasi Umum** tab
   (**NPWP**, **NIK**, **Alamat**, **PTKP Kategori**, **Jabatan**, etc.) from the newly
   selected partner. Changing **Company**, **Wajib Pajak**, **Period Awal**, or **Period
   Akhir** re-fills the income/deduction fields on the **Penghasilan Bruto**,
   **Pengurangan**, and **Penghitungan PPh Pasal 21** tabs from the company's Form 1721
   A1 configuration — for example after correcting the selected **Wajib Pajak**. Any
   manual change made on those fields before the trigger is overwritten.
5. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- Computed fields (**JUMLAH PENGHASILAN BRUTO**, **JUMLAH PENGURANGAN**, **JUMLAH
  PENGHASILAN NETO**, and so on) recalculate automatically.
