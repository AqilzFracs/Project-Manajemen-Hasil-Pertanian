from tabulate import tabulate
import csv

class RedBlackTreeNode:
    def __init__(self, nama, jumlah, color, left=None, right=None, parent=None):
        self.nama = nama
        self.jumlah = jumlah
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent

class RedBlackTree:
    def __init__(self, data_file="hasilPertanian.csv"):
        self.NIL = RedBlackTreeNode(None, None, 0)
        self.root = self.NIL             
        self.load_from_file(data_file)

    def insert(self, nama, jumlah):
        new_node = RedBlackTreeNode(nama, jumlah, 1, self.NIL, self.NIL, self.NIL)
        self._insert_node(self.root, new_node)
        self._fix_insert(new_node)

    def _insert_node(self, root, new_node):
        if root == self.NIL:
            self.root = new_node
        elif new_node.nama < root.nama:
            if root.left == self.NIL:
                root.left = new_node
                new_node.parent = root
            else:
                self._insert_node(root.left, new_node)
        else:
            if root.right == self.NIL:
                root.right = new_node
                new_node.parent = root
            else:
                self._insert_node(root.right, new_node)

    def _fix_insert(self, node):
        while node.parent.color == 1:
            if node.parent == node.parent.parent.left:
                y = node.parent.parent.right
                if y.color == 1:
                    node.parent.color = 0
                    y.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.right_rotate(node.parent.parent)
            else:
                y = node.parent.parent.left
                if y.color == 1:
                    node.parent.color = 0
                    y.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.left_rotate(node.parent.parent)
        self.root.color = 0

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    def search(self, criteria, value):
        return self.search_helper(self.root, criteria, value)
  
    def search_helper(self, node, criteria, value):
        print(f"Current Node: {node.nama}, {node.jumlah}")
        if criteria == "nama":
            if value.lower() == node.nama.lower():
                return node
            elif value.lower() < node.nama.lower():
                node = node.left
            else:
                node = node.right
        elif criteria == "jumlah":
            # node_jumlah = int(node.jumlah)
            print(f"Comparing {value} with {node.jumlah}")
            if node == self.NIL or value == node.jumlah:
                return node
            if value < node.jumlah:
                return self.search_helper(node.left, criteria, value)
            return self.search_helper(node.right, criteria, value)
                
    def search_and_display(self, criteria, value):
      result = self.search_helper(self.root, criteria, value)
      if result != self.NIL:
          data = self.inorder_traversal(result)
          headers = ["Nama", "Jumlah"]
          print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
      else:
          print("Data tidak ditemukan.")

    def inorder_traversal(self, node, descending=False):
        if node != self.NIL:
            left_data = self.inorder_traversal(node.left, descending)
            current_data = [[node.nama, node.jumlah]]
            right_data = self.inorder_traversal(node.right, descending)

            if descending:
                return right_data + current_data + left_data
            else:
                return left_data + current_data + right_data
        else:
            return []

    def display_data(self, descending=False):
        data = self.inorder_traversal(self.root, descending)
        if data:
            print(tabulate(data, headers=["Nama", "Jumlah"], tablefmt="fancy_grid"))
        else:
            print("Tidak ada data data.")

    def delete(self, criteria, nama):
        node = self.search(criteria, nama)
        if node != self.NIL:
            self.delete_node(node)

    def delete_node(self, node):
        y = node
        y_original_color = y.color
        if node.left == self.NIL:
            x = node.right
            self.transplant(node, node.right)
        elif node.right == self.NIL:
            x = node.left
            self.transplant(node, node.left)
        else:
            y = self.minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self.transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color
        if y_original_color == 0:
            self.fix_delete(x)

    def transplant(self, u, v):
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def fix_delete(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 1:
                    w.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == 0 and w.right.color == 0:
                    w.color = 1
                    x = x.parent
                else:
                    if w.right.color == 0:
                        w.left.color = 0
                        w.color = 1
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = 0
                    w.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == 1:
                    w.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == 0 and w.left.color == 0:
                    w.color = 1
                    x = x.parent
                else:
                    if w.left.color == 0:
                        w.right.color = 0
                        w.color = 1
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = 0
                    w.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0

    def edit(self, old_nama, new_nama, new_jumlah):
        node_to_edit = self.search_helper(self.root, "nama", old_nama)
        if node_to_edit != self.NIL:
            self.delete_node(node_to_edit)
            self.insert(new_nama, new_jumlah)
            print("Data berhasil diperbarui.")
        else:
            print("Data tidak ditemukan.")

    def save_to_file(self, filename="hasilPertanian.csv"):
        data = self.inorder_traversal(self.root)
        with open(filename, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["Nama", "Jumlah"])  # Menulis header
            csv_writer.writerows(data)

    def load_from_file(self, filename="hasilPertanian.csv"):
        try:
            with open(filename, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Mengabaikan baris header
                data = [row for row in csv_reader]

            self.root = self.NIL
            for entry in data:
                nama, jumlah = entry
                self.insert(nama, jumlah)
        except FileNotFoundError:
            print("File tidak ditemukan. Menggunakan data default.")
