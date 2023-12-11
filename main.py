from Gudang_Pertanian import redBlackTree

if __name__ == "__main__":
  tree = redBlackTree()

  while True:
      print("\nMenu:")
      print("1. Tambah Data")
      print("2. Cari Data")
      print("3. Tampilkan Semua Data")
      print("4. Hapus Data")
      print("5. Edit Data")
      print("6. Simpan Data ke File")
      print("0. Keluar")

      choice = int(input("Pilih menu: "))

      if choice == 1:
          tree.display_data(desc = False)
          nama = input("Masukkan nama barang: ")
          jumlah = int(input("Masukkan jumlah barang: "))
          harga = int(input("Masukkan harga barang: "))
          tree.insert(nama, jumlah, harga)
      elif choice == 2:
          print("Mencari hasil pertanian berdasarkan")
          print("[1] Nama")
          print("[2] Jumlah")
          print("[3] Harga")
          pilih = int(input("--> "))
          if pilih == 1:
              nama = input("Masukkan nama untuk mencari hasil pertanian: ")
              tree.search_and_display("nama", nama)
          elif pilih == 2:
              jumlah = int(input("Masukkan jumlah untuk mencari hasil pertanian: "))
              tree.search_and_display("jumlah", jumlah)
          elif pilih == 3:
              harga = int(input("Masukkan harga untuk mencari hasil pertanian: "))
              tree.search_and_display("harga", harga)
          else:
              print("invalid input")
      elif choice == 3:
          print("Tampilkan Berdasarkan")
          print("1. Ascending")
          print("2. Descending")
          pilih = int(input("--> "))
          if pilih == 1:
              tree.display_data(desc=False)
          elif pilih == 2:
              tree.display_data(desc=True)
          else:
              print("invalid input")
      elif choice == 4:
          tree.display_data(desc=False)
          nama = input("Masukkan nama untuk menghapus hasil pertanian: ")
          tree.delete(nama)
      elif choice == 5:
          tree.display_data(desc=False)
          nama = input("Masukkan nama untuk mengedit hasil pertanian: ")
          result = tree.search(nama)
          if result != tree.NIL:
              new_nama = input("Masukkan nama baru: ")
              result.value = new_nama
              print("Data diedit.")
          else:
              print("Data tidak ditemukan.")
      elif choice == 6:
          konfirmasi = input("Apakah anda yakin ingin menyimpan perubahan ? (y/n)")
          if konfirmasi == "y":
              filename = "hasilPertanian.csv"
              tree.save_to_file(filename)
              print("Data disimpan ke file.")
          elif konfirmasi == "n":
              print("Kembali ke menu")
              continue
          else:
              print("Invalid Input!")
      elif choice == 0:
          break
      else:
          print("Pilihan tidak valid. Silakan coba lagi.")
