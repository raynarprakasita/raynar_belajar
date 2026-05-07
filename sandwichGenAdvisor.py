import math


# fungsi ngerapihin format dan tampilan
def rupiah(nominal):
  return f"Rp {nominal:,.0f}".replace(",", ".") # nol angka di belakang koma (pembulatan) dan menggantu koma menjadi titik untuk rupiah

def persen(nilai, desimal=1):
  return f"{nilai:.{desimal}f}%" # satu angka dibelakang koma(pembulatan) untuk perhitungan rasio dan bunga/inflasi

def garis(karakter="=", panjang=52): # menampilkan garis
  return karakter * panjang

def judul(teks, karakter="=", panjang=52): # menampilkan judul
  print(f"\n{garis(karakter, panjang)}")
  print(f"  {teks}")
  print(garis(karakter, panjang))


# fungsi input
def input_angka(prompt, min_val=0, boleh_nol=True):
  # validasi input dan antidipasi error
  while True:
    try:
      nilai = int(input(prompt))
      if not boleh_nol and nilai == 0:
        print("  * Nilai tidak boleh nol. Coba lagi.")
        continue
      if nilai < min_val:
        print(f"  * Nilai minimal adalah {rupiah(min_val)}. Coba lagi.")
        continue
      return nilai
    except ValueError:
      print("  * Masukkan angka bulat yang valid (tanpa titik/koma). Coba lagi.")

def input_pilihan(pilihan_valid): # validasi pilihn menu simulasi
  while True:
    pilihan = int(input("  Pilihan Anda (1-6): "))
    if pilihan in pilihan_valid:
      return pilihan
    print(f"  * Pilihan tidak tersedia. Masukkan salah satu dari: {pilihan_valid}")

def konfirmasi(prompt): # konfirmasi simulasi
  return input(prompt).lower()


# fungsi hitung status dan pembuatan rekomendasi
def hitung_status(rasio, batas_aman, batas_bahaya):
  if rasio >= batas_bahaya:
    return "Bahaya", 0
  elif rasio >= batas_aman:
    return "Waspada", 15
  else:
    return "Aman", 25

def buat_rekomendasi(jenis, status, prioritas, perhatian, saran):
  pesan = {
    "pengeluaran": {
      "Bahaya":   "Pengeluaran Anda melampaui 70% pemasukan. Segera pangkas biaya yang tidak mendesak.",
      "Waspada":  "Pengeluaran menyentuh zona waspada (50–70%). Pertimbangkan menunda pembelian barang tidak penting.",
      "Aman":     "Pengeluaran terkendali di bawah 50%. Manfaatkan saldo lebih untuk berinvestasi serta menabung dana pendidikan dan pensiun."
    },
    "hutang": {
      "Bahaya":   "Rasio hutang berada di level kritis. Segera prioritaskan pelunasan sebelum bunga majemuk semakin membebani.",
      "Waspada":  "Rasio hutang masih di zona waspada. Jangan remehkan efek bunga majemuk dalam jangka panjang.",
      "Aman":     "Anda bebas dari hutang. Pertahankan kondisi ini dan hindari hutang berbunga tinggi."
    },
    "dana pendidikan": {
      "Bahaya":   "Progres dana pendidikan masih jauh dari target. Segera tingkatkan alokasi tabungan.",
      "Waspada":  "Progres dana pendidikan sedang. Pertimbangkan menambah nominal tabungan secara berkala.",
      "Aman":     "Progres dana pendidikan berjalan baik. Pertahankan dan pertimbangkan instrumen investasi untuk mempercepat pencapaian."
    },
    "dana pensiun": {
      "Bahaya":   "Progres dana pensiun masih jauh dari target. Segera tingkatkan alokasi sebelum terlambat.",
      "Waspada":  "Progres dana pensiun sedang. Tingkatkan konsistensi menabung untuk masa tua yang lebih aman.",
      "Aman":     "Progres dana pensiun berjalan baik. Teruskan dan optimalkan melalui instrumen investasi jangka panjang."
    }
  }
  teks = f"{pesan[jenis][status]}"
  if status == "Bahaya":
    prioritas.append(teks)
  elif status == "Waspada":
    perhatian.append(teks)
  else:
    saran.append(teks)

def tampilkan_rekomendasi(jenis_rekomendasi, daftar):
  print(f"\n  [{jenis_rekomendasi}]")
  if len(daftar) == 0:
    print("  Tidak ada catatan untuk saat ini.")
  else:
    for item in daftar:
      print(f"  - {item}")


# fungsi simulasi
def simulasi(pilihan, nominal, data, rasio):
  if pilihan == 1:
    judul("SIMULASI: TAMBAH DANA ORANG TUA")
    rasio_baru = ((data["total_pengeluaran"] + nominal) / data["pemasukan"]) * 100

    if rasio["pengeluaran_rasio"] >= 70:
      print("\n  PERINGATAN: Pengeluaran Anda sudah melampaui batas bahaya (70%).")
      print("     Menambah tanggungan orang tua sangat tidak disarankan saat ini.")
    elif rasio["pengeluaran_rasio"] >= 50:
      print("\n  PERHATIAN: Pengeluaran Anda sudah di zona waspada.")
      print("     Pertimbangkan matang-matang sebelum menambah tanggungan.")
    else:
      print("\n  Pengeluaran masih di zona aman. Penambahan masih memungkinkan.")

    print(f"\n  - Rasio pengeluaran saat ini : {persen(rasio['pengeluaran_rasio'])}")
    print(f"  - Rasio pengeluaran setelah  : {persen(rasio_baru)}")

    biaya_peluang = nominal * ((1 + 0.1) ** 5)
    print(f"\n  [Biaya Peluang — Opportunity Cost]")
    print(f"  - Jika {rupiah(nominal)} dialihkan ke investasi 10%/thn selama 5 tahun,")
    print(f"  - Anda berpotensi mendapatkan {rupiah(biaya_peluang)}.")

  elif pilihan == 2 or pilihan == 3:
    if pilihan == 2:
      jenis = "Dana Pendidikan Anak"
      jenis_target  = "pendidikan_target"
      jenis_skrng    = "pendidikan_sekarang"
    else:
      jenis = "Dana Pensiun"
      jenis_target  = "dapen_target"
      jenis_skrng    = "dapen_sekarang"


    judul(f"SIMULASI: NABUNG {jenis.upper()}")

    target = data[jenis_target]
    sekarang = data[jenis_skrng]
    sisa_target = target - sekarang


    waktu = math.ceil(sisa_target / nominal)  # dalam bulan dibulatkan ke atas
    tahun = waktu // 12
    bulan = waktu % 12

    inflasi_tahunan   = 0.05
    return_investasi  = 0.015   #  asumsikan 1.5% per bulan

    # skenario 1: tanpa investasi
    print(f"\n  [Skenario A: Dana Disimpan Tanpa Investasi]")
    target_inflasi = target * ((1 + inflasi_tahunan) ** (waktu / 12))
    selisih_daya_beli = target_inflasi - target

    print(f"  - Estimasi waktu mencapai target   : {tahun} tahun {bulan} bulan")
    print(f"  - Dana terkumpul (nominal)         : {rupiah(target)}")
    print(f"  - Kebutuhan nyata (inflasi 5%/thn) : {rupiah(target_inflasi)}")
    print(f"  - Kekurangan daya beli             : {rupiah(selisih_daya_beli)}")

    # skenario 2: dengan investasi
    print(f"\n  [Skenario B: Dana Dialihkan ke Investasi {persen(return_investasi*100)}/bln]")
    dana_sementara = 0
    for i in range(waktu):
      dana_sementara = (dana_sementara + nominal) * (1 + return_investasi)
    dana_sementara += sekarang
    selisih_investasi = dana_sementara - target

    print(f"  - Proyeksi dana setelah {tahun} thn {bulan} bln : {rupiah(dana_sementara)}")
    print(f"  - Selisih dibanding target          : {rupiah(selisih_investasi)}")

    if pilihan == 3: # jika pilihan 3 (nabung dapen)
      bulan_cukup = int(dana_sementara // data["total_pengeluaran"])
      print(f"\n  * Proyeksi dana pensiun cukup untuk {bulan_cukup} bulan pengeluaran.")

    print("  * Besar imbal hasil investasi beragam, sesuaikan dengan profil risiko Anda.")

  elif pilihan == 4:
    judul("SIMULASI: AMBIL CICILAN BARU")
    bunga = input_angka("  Bunga cicilan baru per bulan (%): ", boleh_nol=False)
    data["bunga_cicilan_baru"] = bunga
    pinjaman_awal = nominal
    rasio_hutang_baru = ((data["hutang"] + nominal) / data["pemasukan"]) * 100

    if rasio["hutang_rasio"] >= 20:
      print("\n  PERINGATAN: Rasio hutang Anda sudah di zona bahaya.")
      print("     Sangat tidak disarankan menambah cicilan baru saat ini.")
    elif rasio["hutang_rasio"] >= 1:
      print("\n  PERHATIAN: Anda masih memiliki cicilan berjalan.")
      print("     Pastikan cicilan baru tidak memberatkan arus kas Anda.")

    print(f"\n  - Pinjaman awal                      : {rupiah(pinjaman_awal)}")
    print(f"  - Bunga per bulan                    : {persen(bunga)}")
    print(f"  - Rasio hutang setelah cicilan baru  : {persen(rasio_hutang_baru)}")

    # visualisai pertumbuhan cicilan tiap bulan (selama 5 bulan)
    print(f"\n  {'Bulan':<11} | {'Total Cicilan':>17}")
    print(f"  {'-'*11}-+-{'-'*17}")
    total_cicilan = pinjaman_awal
    for i in range(5):
      total_cicilan = total_cicilan * (1 + (bunga / 100))
      print(f"  Bulan ke-{i + 1:<2} | {rupiah(total_cicilan):>18}")

    total_bunga = total_cicilan - pinjaman_awal
    print(f"\n  - Pokok pinjaman                   : {rupiah(pinjaman_awal)}")
    print(f"  - Total pelunasan di bulan ke-5    : {rupiah(total_cicilan)}")
    print(f"  - Total bunga yang harus dibayar   : {rupiah(total_bunga)}")

    biaya_peluang = total_bunga * ((1 + 0.015) ** 5)
    print(f"\n  [Biaya Peluang — Opportunity Cost]")
    print(f"  - Jika {rupiah(total_bunga)} (besar bunga) diinvestasikan 1.5%/bln,")
    print(f"  - dalam 5 bulan bisa menjadi {rupiah(biaya_peluang)}.")

  elif pilihan == 5:
    judul("SIMULASI: BAYAR HUTANG")
    sisa = data["hutang"]
    bunga = data["bunga"] / 100
    total_bayar_awal = 0
    bulan_awal = 0
    while sisa > 0:
      if sisa < nominal:
        total_bayar_awal += sisa
        bulan_awal += 1
        sisa = 0
      else:
        sisa = (sisa - nominal) * (1 + bunga)
        total_bayar_awal += nominal
        bulan_awal += 1
        if bulan_awal > 10000: # antisipasi infinite loop
          print("  * Nominal terlalu kecil untuk melunasi hutang. Simulasi dihentikan.")
          return
    tahun = bulan_awal // 12
    bulan = bulan_awal % 12
    print(f"  - Estimasi waktu sampai lunas   : {tahun} tahun {bulan} bulan")
    print("  * Asumsi bayar di awal bulan")


    nominal_plus = nominal * 1.05 # skenario cicilan bulanan nambah 5%
    sisa = data["hutang"]
    total_bayar_plus = 0
    bulan_plus = 0
    while sisa > 0:
      if sisa < nominal_plus:
        total_bayar_plus += sisa
        bulan_plus += 1
        sisa = 0
      else:
        sisa = (sisa - nominal_plus) * (1 + bunga)
        total_bayar_plus += nominal_plus
        bulan_plus += 1
        if bulan_plus > 10000: # antisipasi infinite loop
          print("  * Nominal terlalu kecil untuk melunasi hutang. Simulasi dihentikan.")
          return

    selisih_bulan = bulan_awal - bulan_plus
    selisih_total = total_bayar_awal - total_bayar_plus

    print(f"\n  - Sisa hutang saat ini             : {rupiah(data['hutang'])}")
    print(f"  - Bunga per bulan                  : {persen(data['bunga'])}")
    print()
    print(f"  {'':30} {'Skenario Awal':>14} {'+ 5% Cicilan':>14}")
    print(f"  {'-'*30}-{'-'*14}-{'-'*14}")
    print(f"  {'- Cicilan per bulan':<30} {rupiah(nominal):>14} {rupiah(nominal_plus):>14}")
    print(f"  {'- Lama pelunasan':<30} {str(bulan_awal) + ' bln':>14} {str(bulan_plus) + ' bln':>14}")
    print(f"  {'- Total pembayaran':<30} {rupiah(total_bayar_awal):>14} {rupiah(total_bayar_plus):>14}")
    print()
    print(f"  * Dengan menambah 5% cicilan, hutang lunas {selisih_bulan} bulan lebih cepat")
    print(f"    dan Anda hemat {rupiah(selisih_total)} dari total pembayaran.")
    print("  * Asumsi bayar di awal bulan")


# fungsi utama

def main():
  print(garis("═", 52))
  print("      SANDWICH GEN ADVISOR — Literasi Finansial")
  print("   Solusi cerdas untuk Generasi Sandwich Indonesia")
  print(garis("═", 52))

  # input data pengguna
  print("\n  Masukkan data keuangan Anda dengan teliti.")
  print("  (Gunakan angka bulat, tanpa titik atau koma)\n")

  data = {}
  data["nama"]      = input("  Nama Anda                          : ")
  data["pemasukan"] = input_angka("  Pemasukan bulanan (Rp)             : ", boleh_nol=False) # antisipasi zero division

  print("\n  --- Pengeluaran Bulanan ---")
  data["tanggung_ortu"]  = input_angka("  Tanggungan orang tua (Rp)          : ")
  data["rumah_tangga"]   = input_angka("  Tanggungan rumah tangga (Rp)       : ", boleh_nol=False) # asumsikan pengeluaran rumah tangga tidak mungkin nol agar tidak eror
  data["anak"]           = input_angka("  Tanggungan anak (Rp)               : ")

  print("\n  --- Dana Pendidikan Anak ---")
  data["pendidikan_target"]  = input_angka("  Target dana pendidikan (Rp)        : ", boleh_nol=False)
  data["pendidikan_sekarang"]= input_angka("  Dana pendidikan terkumpul (Rp)     : ")

  print("\n  --- Dana Pensiun ---")
  data["dapen_target"]   = input_angka("  Target dana pensiun (Rp)           : ", boleh_nol=False)
  data["dapen_sekarang"] = input_angka("  Dana pensiun terkumpul (Rp)        : ")

  print("\n  --- Hutang & Cicilan ---")
  data["hutang"] = input_angka("  Total pokok hutang/cicilan (Rp)    : ")
  if data["hutang"] > 0:
    data["bunga"] = input_angka("  Bunga hutang per bulan (%): ", boleh_nol=False)
  else:
    data["bunga"] = 0
  data["total_pengeluaran"] = data["tanggung_ortu"] + data["rumah_tangga"] + data["anak"]
  


  # loop utama
  while True:
    # agar rasio selalu update
    data["sisa"] = data["pemasukan"] - data["total_pengeluaran"]
    rasio = {}
    rasio["pengeluaran_rasio"] = (data["total_pengeluaran"] / data["pemasukan"]) * 100
    rasio["hutang_rasio"] = (data["hutang"] / data["pemasukan"]) * 100
    rasio["prog_anak"]  = ((data["pendidikan_target"] - data["pendidikan_sekarang"]) / data["pendidikan_target"]) * 100
    rasio["prog_dapen"] = ((data["dapen_target"] - data["dapen_sekarang"]) / data["dapen_target"]) * 100

    # analisis kesehatan keuangan
    health_score = 0
    prioritas, perhatian, saran = [], [], []

    status_pengeluaran, skor_pengeluaran = hitung_status(rasio["pengeluaran_rasio"], 50, 70)
    health_score += skor_pengeluaran
    buat_rekomendasi("pengeluaran", status_pengeluaran, prioritas, perhatian, saran)

    status_hutang, skor_hutang = hitung_status(rasio["hutang_rasio"], 1, 20)
    health_score += skor_hutang
    buat_rekomendasi("hutang", status_hutang, prioritas, perhatian, saran)

    status_anak, skor_anak = hitung_status(rasio["prog_anak"], 30, 70)
    health_score += skor_anak
    buat_rekomendasi("dana pendidikan", status_anak, prioritas, perhatian, saran)

    status_dapen, skor_dapen = hitung_status(rasio["prog_dapen"], 30, 70)
    health_score += skor_dapen
    buat_rekomendasi("dana pensiun", status_dapen, prioritas, perhatian, saran)

    # dashboard
    judul(f"DASHBOARD KEUANGAN — {data['nama'].upper()}")
    print(f"\n  {'Komponen':<30} {'Nilai':>10}  {'Status':>8}")
    print(f"  {'-'*30}  {'-'*10}  {'-'*8}")
    print(f"  {'Rasio Pengeluaran':<30} {persen(rasio['pengeluaran_rasio']):>10}  {status_pengeluaran:>8}  [{skor_pengeluaran}/25]")
    print(f"  {'Rasio Hutang':<30} {persen(rasio['hutang_rasio']):>10}  {status_hutang:>8}  [{skor_hutang}/25]")
    print(f"  {'Progres Dana Pendidikan':<30} {persen(100 - rasio['prog_anak']):>10}  {status_anak:>8}  [{skor_anak}/25]")
    print(f"  {'Progres Dana Pensiun':<30} {persen(100 - rasio['prog_dapen']):>10}  {status_dapen:>8}  [{skor_dapen}/25]")
    print(f"\n  {'Financial Health Score':.<35} {health_score}/100")
    print(f"  {'Sisa Pemasukan Bulanan':.<35} {rupiah(data['sisa'])}")

    # rekomendasi
    judul("REKOMENDASI", "-", 52)
    tampilkan_rekomendasi("🔴 Prioritas", prioritas)
    tampilkan_rekomendasi("⚠️ Perhatian", perhatian)
    tampilkan_rekomendasi("✅ Saran", saran)

    # menu simulasi
    judul("MENU SIMULASI", "-", 52)
    print("  1. Tambah Dana Orang Tua      2. Nabung Dana Pendidikan")
    print("  3. Nabung Dana Pensiun        4. Ambil Cicilan Baru")
    print("  5. Bayar Hutang               6. Keluar")
    print()

    pilihan = input_pilihan(list(range(1,7)))

    if pilihan == 6:
      print(f"\n  Terima kasih, {data['nama']}!")
      if data["sisa"] > 0:
        data["dapen_sekarang"] += data["sisa"]
        print(f"  - Sisa saldo {rupiah(data['sisa'])} dialokasikan ke dana pensiun Anda.")
        print(f"  - Total dana pensiun akhir: {rupiah(data['dapen_sekarang'])}")
        print(f"\n  * Tetap semangat meraih kebebasan finansial!")
        print(garis("═", 52))
      break

    # validasi data hutang untuk menu 5
    if pilihan == 5 and data["hutang"] == 0:
      print("\n  * Selamat! Anda tidak memiliki hutang saat ini.")
      input("  (Tekan Enter untuk kembali ke menu...)")
      continue

    # input nominal
    input_nominal = {
      "1": "  Tambahan dana orang tua (Rp): ",
      "2": "  Nominal tabungan pendidikan per bulan (Rp): ",
      "3": "  Nominal tabungan pensiun per bulan (Rp): ",
      "4": "  Nominal cicilan baru(Rp): ",
      "5": "  Nominal pembayaran hutang per bulan (Rp): "
    }
    nominal = input_angka(input_nominal[str(pilihan)], boleh_nol=False)

    # jalankan simulasi
    simulasi(pilihan, nominal, data, rasio)

    # konfirmasi & terapkan keputusan
    print()
    yakin = konfirmasi("  Apakah Anda yakin dengan keputusan ini? (y/n): ")
    if yakin == "y":
      if pilihan == 1:
        while nominal > data["sisa"]:
          print(f"  * Nominal melebihi sisa pemasukan ({rupiah(data['sisa'])}).")
          nominal = input_angka("  Masukkan nominal yang valid (Rp): ", boleh_nol=False)
        data["tanggung_ortu"] += nominal
        data["total_pengeluaran"] += nominal
        print(f"  * Tanggungan orang tua diperbarui menjadi {rupiah(data['tanggung_ortu'])}")

      elif pilihan == 2:
        while nominal > data["sisa"]:
          print(f"  * Nominal melebihi sisa pemasukan ({rupiah(data['sisa'])}).")
          nominal = input_angka("  Masukkan nominal yang valid (Rp): ", boleh_nol=False)
        data["pendidikan_sekarang"] += nominal
        data["total_pengeluaran"] += nominal
        print(f"  * Dana pendidikan diperbarui menjadi {rupiah(data['pendidikan_sekarang'])}")
        print("  * Proyeksi pertumbuhan investasi tidak disimpan di saldo dana pendidikan.")

      elif pilihan == 3:
        while nominal > data["sisa"]:
          print(f"  * Nominal melebihi sisa pemasukan ({rupiah(data['sisa'])}).")
          nominal = input_angka("  Masukkan nominal yang valid (Rp): ", boleh_nol=False)
        data["dapen_sekarang"] += nominal
        data["total_pengeluaran"] += nominal
        print(f"  * Dana pensiun diperbarui menjadi {rupiah(data['dapen_sekarang'])}")
        print("  * Proyeksi pertumbuhan investasi tidak disimpan di saldo dana pendidikan.")

      elif pilihan == 4:
        bunga_baru = data["bunga_cicilan_baru"]
        if bunga_baru > data["bunga"]:
          data["bunga"] = bunga_baru  # gunakan bunga tertinggi (skenario terburuk)
        data["hutang"] += nominal
        print(f"  * Total hutang diperbarui menjadi {rupiah(data['hutang'])}")

      elif pilihan == 5:
        while nominal > data["hutang"] or nominal > data["sisa"]:
          print(f"  * Nominal melebihi sisa hutang ({rupiah(data['hutang'])}) atau sisa pemasukan ({rupiah(data['sisa'])}).")
          nominal = input_angka("  Masukkan nominal yang valid (Rp): ", boleh_nol=False)
        data["hutang"] -= nominal
        data["total_pengeluaran"] += nominal
        print(f"  * Sisa hutang diperbarui menjadi {rupiah(data['hutang'])}")
        if data["hutang"] == 0:
          print("  Selamat! Hutang Anda telah lunas!")

    else:
      print("  Keputusan dibatalkan. Tidak ada perubahan data.")

    input("\n  (Tekan Enter untuk kembali ke menu...)")

main()