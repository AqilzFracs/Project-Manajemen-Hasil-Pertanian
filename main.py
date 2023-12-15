from Gudang_Pertanian import RedBlackTree
import csv
from prettytable import PrettyTable
from tabulate import tabulate

if __name__ == "__main__":
  rb_tree = RedBlackTree()

  with open("hasilPertanian.csv", 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            data = [row for row in csv_reader]

            for i in data:
                rb_tree.insert(i[0], i[1])

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
        rb_tree.display_data()
        nama = input("Masukkan nama barang: ")
        jumlah = int(input("Masukkan jumlah barang: "))
        rb_tree.insert(nama, jumlah)
      elif choice == 2:
          print("Mencari hasil pertanian berdasarkan")
          print("[1] Nama")
          print("[2] Jumlah")
          pilih = int(input("--> "))
          if pilih == 1:
            nama = input("Masukkan nama untuk mencari hasil pertanian: ")
            result_node = rb_tree.search_key(nama)
            if result_node != rb_tree.NIL:
                data = [[result_node.key, result_node.value]]
                print(tabulate(data, headers=["Nama", "Jumlah"], tablefmt='fancy_grid'))
            else:
                print(f"\nNilai '{nama}' tidak ditemukan dalam pohon.")
          elif pilih == 2:
              jumlah = input("Masukkan jumlah untuk mencari hasil pertanian: ")
              result_nodes = rb_tree.search_value(jumlah)
              if result_nodes != rb_tree.NIL:
                data = [[node.key, node.value] for node in result_nodes]
                print(tabulate(data, headers=["Nama", "Jumlah"], tablefmt='fancy_grid'))
              else:
                print(f"\nNilai '{jumlah}' tidak ditemukan dalam pohon.")
          else:
              print("invalid input")
      elif choice == 3:
          print("Tampilkan Berdasarkan")
          print("1. Ascending")
          print("2. descending")
          pilih = int(input("--> "))
          if pilih == 1:
            rb_tree.display_data()
          elif pilih == 2:
            rb_tree.display_data(descending=True)
          else:
              print("invalid input")
      elif choice == 4:
        rb_tree.display_data()
        nama = input("Masukkan nama untuk menghapus hasil pertanian: ")
        rb_tree.delete(nama)
      elif choice == 5:
        rb_tree.display_data()
        nama = input("Masukkan nama hasil pertanian untuk mengedit: ")
        new_nama = input("Masukkan nama baru: ")
        new_jumlah = input("Masukkan jumlah baru: ")
        rb_tree.edit(nama, new_nama, new_jumlah)
      elif choice == 6:
          konfirmasi = input("Apakah anda yakin ingin menyimpan perubahan ? (y/n)")
          if konfirmasi == "y":
              filename = "hasilPertanian.csv"
              rb_tree.save_to_file()
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
