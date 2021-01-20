# Twitter Sentiment Analysis Project

Project ini bertujuan untuk membuat sebuah UI untuk melakukan penyimpanan, processing, dan Analisa data dari twitter

App terdiri dari lima buah menu (Update data, Update Nilai sentiment, Lihat data, Visualisasi, dan Keluar)

1. Pada Menu Update Data
- Menggunakan satu kata kunci “vaksin covid”
- Akan menjalankan fungsi untuk mengupdate data pada range tanggal tertentu.
- Melakukan pre-processing
- Data dimasukkan pada tabel SQL

2. Pada Menu Update Nilai Sentiment
- Memproses semua data tweet yang telah diambil yang belum memiliki nilai sentiment dengan fungsi analysis sentiment
- Update nilai sentiment pada tabel sql

3. Pada Menu lihat data
- Terdapat input range tanggal
- Mengambil data dari tabel sql sesuai range tanggal yang dipilih
- Menampilkan akun user, tanggal tweet, dan tweet

4. Pada Menu Visualisasi
- Terdapat input range tanggal
- Mengambil data dari tabel sql sesuai range tanggal yang dipilih
- Melakukan pengambilan nilai sentimen
- Menampilkan nilai rata-rata, median, dan standar deviasi.
- Menampilkan plot
