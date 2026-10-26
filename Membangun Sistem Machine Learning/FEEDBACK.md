# Feedback Reviewer

## Tanggal Submit
Selasa, 25 November 2025 - 19:28:11

## Rating
⭐⭐⭐⭐⭐ (5/5 Bintang)

## Komentar Umum
Hallo zidanmubarak!, Selamat! Kamu telah berhasil menyelesaikan tugas untuk Proyek Akhir. Dengan demikian kamu telah berhasil membuat sistem machine learning secara utuh.

Terima kasih telah sabar menunggu. Kami membutuhkan waktu untuk bisa memberikan feedback yang komprehensif. Untuk meningkatkan kualitas project submission yang dikirimkan, kamu dapat menerapkan beberapa saran berikut:

**Overall Review:**
- [Kriteria 1: Melakukan Eksperimen Terhadap Dataset Pelatihan] - Advanced
- [Kriteria 2: Membangun Model Machine Learning] - Advanced
- [Kriteria 3: Membuat Workflow CI] - Advanced
- [Kriteria 4: Membuat Sistem Monitoring dan Logging] - Advanced

**Nilai Akhir : Advanced (4)**

## Yang Sudah Baik
- **Kriteria 1: Melakukan Eksperimen Terhadap Dataset Pelatihan [Advanced]**: Berhasil melakukan eksperimen terhadap dataset pelatihan dengan standar tingkat lanjut.
- **Kriteria 2: Membangun Model Machine Learning [Advanced]**: Berhasil membangun model machine learning lengkap dengan manual logging, metrik evaluasi mendalam, tuning hyperparameter, dan artefak terintegrasi.
- **Kriteria 3: Membuat Workflow CI [Advanced]**: Berhasil membangun pipeline dan workflow Continuous Integration (CI) secara otomatis.
- **Kriteria 4: Membuat Sistem Monitoring dan Logging [Advanced]**: Berhasil membangun sistem monitoring dan logging menyeluruh (Prometheus & Grafana) beserta konfigurasi alerting dan model serving.

## Saran Perbaikan
- **Implementasi A/B Testing & Canary Deployment**: Eksplorasi teknik deployment dinamis untuk membandingkan performa model secara paralel dan melakukan gradual rollout model baru. Integrasikan dengan Docker dan CI/CD pipeline yang sudah ada untuk pengujian lebih aman. Referensi: [Exploring Blue & Green Deployment, A/B Testing and Canary Release](https://medium.com/@kazimozkabadayi/exploring-blue-green-deployment-a-b-testing-and-canary-release-161c5e588de0)
- **Integrasi Deteksi Data Drift Otomatis**: Perluas sistem monitoring Prometheus/Grafana dengan penambahan real-time drift detection untuk fitur kritis dan degradasi performa model menggunakan metrik statistik seperti Kullback-Leibler divergence.
- **Pengembangan Automated Testing Pipeline**: Bangun custom testing framework di GitHub Actions khusus untuk validasi data (skema/distribusi), stabilitas model, dan backward compatibility sebelum deployment.
- **Konstruksi Feature Store Terpusat**: Desain repositori terpusat untuk manajemen fitur lintas training/serving guna menjamin konsistensi fitur dan mengurangi training-serving skew. Referensi: [Feast: Open-Source Feature Store](https://docs.feast.dev/)
- **Versioning Data & Model Terintegrasi**: Kombinasikan DVC (Data Version Control) dengan MLFlow/DAGsHub untuk tracking perubahan dataset dan model secara simultan dalam eksperimen. Referensi: [DVC Get Started Guide](https://dvc.org/doc/start)
- **Security Hardening Pipeline**: Implementasi praktik keamanan MLOps: scanning vulnerability container, secret management, dan RBAC (Role-Based Access Control) di MLFlow/Grafana. Referensi: [OWASP ML Security Checklist](https://owasp.org/www-project-machine-learning-security-top-10/)

## Catatan Tambahan
Pada penilaian dengan skema Mastery-Grading, penilaian dilakukan secara berjenjang. Artinya, jika kriteria Skilled tidak terpenuhi, maka keberhasilan dalam menerapkan kriteria Advanced tidak akan dianggap sah. Dengan kata lain, penerapan pada tingkat lanjut akan dinyatakan tidak valid apabila tahapan sebelumnya belum dipenuhi dengan benar.
