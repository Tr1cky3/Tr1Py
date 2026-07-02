# Mini Compiler: Analisis Bahasa Kustom hingga Three-Address Code (TAC)

Proyek ini adalah implementasi *mini compiler* modular yang dirancang untuk mengenali, memvalidasi, dan menerjemahkan bahasa pemrograman Tr1Py dengan sintaksis sendiri ke dalam bentuk Kode Antara (**Three-Address Code / TAC**).

## Mahasiswa

* **Nama:** Anshorullah
* **NIM:** 231011401467
* **Kelas:** 06TPLM002

---

## 🛠️ Karakteristik & Sintaksis Bahasa Kustom

Bahasa Tr1Py ini memiliki aturan leksikal dan sintaksis unik yang berbeda dari bahasa pemrograman konvensional:

* **Penugasan Variabel:** Menggunakan simbol `=` (contoh: `skor = 15`).
* **Kondisi `jika`:** Menggunakan penanda khusus `:` di awal kondisi dan `;` di akhir kondisi.
* **Pembuka & Penutup Blok:** Menggunakan karakter tunggal `p` untuk membuka blok (`{`) dan `q` untuk menutup blok (`}`).
* **Fungsi Output:** Menggunakan perintah `keluaran:ekspresi;`.

### Contoh Kode Sumber

```text
skor = 15
jika :skor < 20; p
    keluaran:skor;
q selain p
    keluaran:0;
q

```

---

## Arsitektur & Alur Kompilasi

Program ini dibangun secara modular menggunakan bahasa pemrograman Python dengan membaginya ke dalam 4 tahapan utama:

### 1. Analisis Leksikal (`lexer.py`)

Tahap pertama yang bertugas memecah string kode sumber mentah menjadi rangkaian objek komponen terkecil bernama **Tokens**. Menggunakan mesin pencocokan pola Regular Expression (Regex) dengan aturan prioritas token (seperti memprioritaskan karakter pembuka blok `p`/`q` di atas identifier biasa agar tidak terjadi salah deteksi).

### 2. Analisis Sintaksis (`parser.py`)

Menggunakan algoritma *Recursive Descent Parser* untuk memeriksa apakah urutan token yang dihasilkan oleh Lexer sudah sesuai dengan tata bahasa (*grammar*) yang ditentukan. Tahap ini menghasilkan **Abstract Syntax Tree (AST)** terstruktur menggunakan Python `@dataclass` seperti:

* `NodeAngka` & `NodeVariabel`
* `NodeOp` (Operasi perbandingan)
* `NodeIsiVar` (Penugasan)
* `NodePercabangan` (Struktur `jika-selain`)
* `NodeKeluaran` (Fungsi cetak)

### 3. Analisis Semantik (`semantic.py`)

Melakukan validasi logika pada AST untuk memastikan kode aman dari kesalahan konteks runtime. Fitur utamanya adalah **Pengecekan Variabel Gaib**, yaitu memastikan sebuah variabel wajib diisi nilainya terlebih dahulu sebelum dipanggil di bagian kode yang lain. Jika melanggar, compiler akan mogok dan melemparkan `NameError`.

### 4. Generasi Kode Antara / TAC (`tac_generator.py`)

Tahap akhir yang bertugas meratakan (*flattening*) struktur pohon AST yang kompleks menjadi instruksi linear tiga alamat (Three-Address Code). Menggunakan fungsi *tree traversal* (Visitor Pattern) untuk menghasilkan instruksi berbasis variabel *temporary* (`t1`, `t2`), `ifFalse`, `goto`, dan label lompatan (`L1`, `L2`).

---

## Cara Menjalankan Program

1. Pastikan seluruh file berikut berada dalam satu folder proyek yang sama:

* `lexer.py`
* `parser.py`
* `semantic.py`
* `tac_generator.py`
* `main.py`

1. Buka terminal atau PowerShell pada direktori proyek tersebut.

2. Jalankan file utama menggunakan perintah:

```bash
py main.py

```

---

## Hasil Output Kompilasi (Terminal)

Ketika `main.py` dieksekusi, compiler akan memamerkan seluruh riwayat pipa kompilasi dari awal hingga menghasilkan instruksi target TAC berikut:

```text
=== MEMULAI PROSES KOMPILASI MINI COMPILER ===

[Tahap 1] Menjalankan Analisis Leksikal...
 -> Sukses. Token berhasil dipecah.

[Tahap 2] Menjalankan Analisis Sintaksis (Parsing AST)...
 -> Sukses. Abstract Syntax Tree (AST) terbentuk.

[Tahap 3] Menjalankan Analisis Semantik...
 -> Sukses. Validasi variabel aman.

[Tahap 4] Menghasilkan Kode Tiga Alamat (Three-Address Code)...

================ HASIL KODE TAC ================
  skor = 15
  t1 = skor < 20
  ifFalse t1 goto L1
  param skor
  call keluaran, 1
  goto L2
  L1:
  param 0
  call keluaran, 1
  L2:
================================================
