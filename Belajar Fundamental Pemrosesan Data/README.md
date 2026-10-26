# Belajar Fundamental Pemrosesan Data

Ini adalah direktori untuk submission pada kelas **Belajar Fundamental Pemrosesan Data** di Dicoding Academy. Proyek akhir ini berfokus pada pembangunan **ETL (Extract, Transform, Load) Pipeline Sederhana** yang dirancang dengan prinsip kode modular serta dilengkapi dengan unit testing menyeluruh.

## Kriteria yang Telah Dipenuhi
- [x] Membuat ETL Pipeline dengan Prinsip Modular Code
- [x] Menyimpan Data dalam Repositori Data
- [x] Menerapkan Unit Test

## Struktur Direktori
- `submission/` : Direktori berkas proyek pipeline ETL:
  - `main.py` : Titik masuk (*entry point*) utama eksekusi pipeline ETL.
  - `utils/` : Modul pemrosesan modular:
    - `extract.py` : Skrip ekstraksi data dari sumber data (CSV).
    - `transform.py` : Skrip pembersihan, manipulasi, dan transformasi data.
    - `load.py` : Skrip untuk memuat dan menyimpan data hasil transformasi ke repositori data target.
  - `tests/` : Pengujian unit test untuk masing-masing modul (`test_extract.py`, `test_transform.py`, `test_load.py`).
  - `products.csv` : Dataset contoh yang digunakan dalam alur pemrosesan data.
  - `requirements.txt` : Daftar dependensi Python yang dibutuhkan.
  - `submission.txt` : Petunjuk menjalankan pipeline ETL, pengujian unit test, dan coverage report.
- `FEEDBACK.md` : Berisi umpan balik (feedback) dan ulasan lengkap dari reviewer terkait hasil penilaian submission.

Untuk melihat umpan balik dari reviewer Dicoding, silakan buka file [FEEDBACK.md](FEEDBACK.md).
