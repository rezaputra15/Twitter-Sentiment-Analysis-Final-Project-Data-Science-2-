# Twitter Sentiment Analysis Project

Project ini bertujuan untuk membuat sebuah UI untuk melakukan penyimpanan, processing, dan Analisa data dari twitter
  • App terdiri dari lima buah menu (Update data, Update Nilai sentiment, Lihat data, Visualisasi, dan Keluar)
  • Pada Menu Update Data
      o Menggunakan satu kata kunci “vaksin covid”
      o Akan menjalankan fungsi untuk mengupdate data pada range tanggal tertentu.
      o Melakukan pre-processing
      o Data dimasukkan pada tabel SQL
  • Pada Menu Update Nilai Sentiment
      o Memproses semua data tweet yang telah diambil yang belum memiliki nilai sentiment dengan fungsi analysis sentiment
      o Update nilai sentiment pada tabel sql
  • Pada Menu lihat data
      o Terdapat input range tanggal
      o Mengambil data dari tabel sql sesuai range tanggal yang dipilih
      o Menampilkan akun user, tanggal tweet, dan tweet
  • Pada Menu Visualisasi
      o Terdapat input range tanggal
      o Mengambil data dari tabel sql sesuai range tanggal yang dipilih
      o Melakukan pengambilan nilai sentimen
      o Menampilkan nilai rata-rata, median, dan standar deviasi.
      o Menampilkan plot
