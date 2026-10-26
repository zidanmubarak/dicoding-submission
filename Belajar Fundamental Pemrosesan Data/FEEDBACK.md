# Feedback Reviewer

## Tanggal Submit
Jumat, 02 Mei 2025 - 22:05:36

## Rating
⭐⭐⭐⭐⭐ (5/5 Bintang)

## Komentar Umum
Hallo zidanmubarak, kami ingin mengucapkan selamat! Karena kamu telah menyelesaikan tugas untuk Proyek Akhir: Membangun ETL Pipeline Sederhana dari kelas Belajar Fundamental Pemrosesan Data.

Terima kasih telah sabar menunggu. Kami membutuhkan waktu untuk bisa memberikan feedback sekomprehensif mungkin kepada setiap peserta kelas. Dalam kesempatan ini ada 2 hal yang ingin kami sampaikan.

Pertama, kamu harus bangga karena telah menyelesaikan submission sesuai dengan kriteria yang ada. Share sertifikat kamu di LinkedIn untuk menunjukkan skill kamu yang telah tervalidasi. Mention @dicoding di media sosial jika ingin memberi inspirasi yang lain.

Kedua, berikut kami sampaikan beberapa catatan dan saran untuk meningkatkan kualitas submission yang kamu kirimkan.

**Nilai Akhir : Advanced**

## Yang Sudah Baik
- **Membuat ETL Pipeline dengan Prinsip Modular Code [Advanced]**: Berhasil merancang pipeline ETL dengan pemisahan modul yang terstruktur, rapi, dan mudah dipelihara.
- **Menyimpan Data dalam Repositori Data [Advanced]**: Berhasil memuat dan menyimpan data hasil transformasi ke repositori data target dengan benar.
- **Menerapkan Unit Test [Advanced]**: Mengimplementasikan unit testing komprehensif pada setiap tahapan ETL (ekstraksi, transformasi, dan pemuatan data).

## Saran Perbaikan & Eksplorasi
- **Manfaatkan Bonobo untuk Membangun Pipeline ETL Modular**: Bonobo adalah framework ETL Python yang ringan dan modular, memungkinkan Anda membangun pipeline data dengan komponen yang dapat digunakan kembali serta mendukung pemrosesan paralel untuk tugas ETL skala kecil hingga menengah. Referensi: [Bonobo Documentation](https://www.bonobo-project.org/)
- **Menyimpan Data dalam Format Apache Parquet**: Format penyimpanan kolumnar yang efisien untuk dataset besar dengan kompresi tinggi dan performa I/O cepat menggunakan library `pyarrow` atau `fastparquet`.
  - Referensi: [PyArrow Parquet Documentation](https://arrow.apache.org/docs/python/parquet.html)
  - Referensi: [Artikel Medium: All About Parquet Part 08](https://medium.com/data-engineering-with-dremio/all-about-parquet-part-08-reading-and-writing-parquet-files-in-python-3b395567eebe)
- **Menyimpan Data ke Google BigQuery**: Manfaatkan data warehouse berbasis cloud untuk analitik data skala besar menggunakan library `google-cloud-bigquery` atau `pandas-gbq`.
  - Referensi: [BigQuery Python Client Documentation](https://cloud.google.com/bigquery/docs/python-libraries)
  - Referensi: [Artikel Medium: How to Write Data Into BigQuery](https://medium.com/@shuvro_25220/how-to-write-data-into-bigquery-if-you-have-to-35e47cd6d80f)
- **Simulasi Negative Case dengan `side_effect` dalam Unit Testing**: Gunakan fitur `side_effect` dari `unittest.mock` untuk mengatur perilaku khusus seperti mensimulasikan kegagalan dependensi eksternal (API timeout atau kegagalan koneksi database) guna menguji ketahanan kode saat menghadapi error. Referensi: [Python Docs - Mock side_effect](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect)

## Saran Belajar Tambahan
- **Pengelolaan Variabel Lingkungan dengan Dotenv**: Hindari menyimpan variabel sensitif seperti credentials atau spreadsheet ID langsung di dalam modul. Gunakan `python-dotenv` untuk menyimpan variabel sensitif di file `.env` secara terpusat dan aman. Referensi: [Using Py Dotenv Package to Manage Env Variables](https://configu.com/blog/using-py-dotenv-python-dotenv-package-to-manage-env-variables/)
- **Kemudahan Integrasi Google Sheets dengan `gspread`**: Pertimbangkan menggunakan library `gspread` sebagai alternatif `googleapiclient.discovery.build` untuk mempermudah akses dokumen spreadsheet berdasarkan nama/URL serta integrasi mulus dengan Pandas DataFrame tanpa konversi manual.
- **Penerapan Style Guide PEP 8**: Terapkan standar penulisan kode [PEP 8](https://peps.python.org/pep-0008/) secara bertahap dan gunakan linter seperti [Flake8](https://flake8.pycqa.org/en/latest/) atau [Pylint](https://www.pylint.org/) untuk menjaga konsistensi kode.
- **Standarisasi Dokumentasi**: Biasakan menambahkan docstring standar [PEP 257](https://peps.python.org/pep-0257/) pada modul, fungsi, dan kelas, serta dokumentasi proyek eksternal yang terstruktur di file `README.md` (menggunakan bantuan [Make a README](https://www.makeareadme.com/)).
