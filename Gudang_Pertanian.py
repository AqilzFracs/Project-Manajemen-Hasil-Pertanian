from tabulate import tabulate as tb
import csv


class Node:
  def __init__(self, nama, jumlah, harga, color = 0, parent = None, left = None, right = None,):
    self.nama = nama
    self.jumlah = jumlah
    self.harga = harga
    self.color = color
    self.parent = parent
    self.left = left
    self.right = right

class redBlackTree:
  def __init__(self, data_file = "hasilPertanian.csv"):
    self.NIL = Node(None, None, None)
    self.root = self.NIL
    self.load_from_file(data_file)

  def insert(self, nama, jumlah, harga):
    new_node = Node(nama, jumlah, harga, 1, self.NIL, self.NIL, self.NIL)
    self.binary_insert(self.root, new_node)
    self.fix_insert(new_node)
  
  def binary_insert(self, root, new_node):
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
  
  def fix_insert(self, node):
    while node.parent.color == 1:  # Parent node is red
      if node.parent == node.parent.parent.right:
        uncle = node.parent.parent.left
        if uncle.color == 1:
            # Case 1: Node's uncle is red
            node.parent.color = 0
            uncle.color = 0
            node.parent.parent.color = 1
            node = node.parent.parent
        else:
            # Case 2: Node's uncle is black and node is a left child
            if node == node.parent.left:
                node = node.parent
                self.right_rotate(node)

            # Case 3: Node's uncle is black and node is a right child
            node.parent.color = 0
            node.parent.parent.color = 1
            self.left_rotate(node.parent.parent)
      else:
        uncle = node.parent.parent.right
        if uncle.color == 1:
            # Case 1: Node's uncle is red
            node.parent.color = 0
            uncle.color = 0
            node.parent.parent.color = 1
            node = node.parent.parent
        else:
            # Case 2: Node's uncle is black and node is a right child
            if node == node.parent.right:
                node = node.parent
                self.left_rotate(node)

            # Case 3: Node's uncle is black and node is a right child
            node.parent.color = 0
            node.parent.parent.color = 1
            self.right_rotate(node.parent.parent)
    self.root.color = 0

  def left_rotate(self, x):
    y = x.right
    x.right = y.left

    if y.left != self.NIL:
        y.left.parent = x

    y.parent = x.parent

    if x.parent is None:
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

    if x.parent is None:
        self.root = y
    elif x == x.parent.right:
        x.parent.right = y
    else:
        x.parent.left = y

    y.right = x
    x.parent = y
  
  def search(self, criteria, value):
    return self.search_helper(self.root, criteria, value)
  
  def search_helper(self, node, criteria, value):
      while node != self.NIL:
        if criteria == "nama":
            if value == node.nama:
              return node
            elif value < node.nama:
              node = node.left
            else:
                node = node.right
        elif criteria == "jumlah":
            if value == node.jumlah:
                return node
            if value < node.jumlah:
                node = node.left
            else:
                node = node.right
        else:
            if value == node.harga:
                return node
            if value < node.harga:
                node = node.left
            else:
                node = node.right

  def search_and_display(self, criteria, value):
      result = self.search_helper(self.root, criteria, value)
      if result != self.NIL:
          data = self.inorder_traversal(result)
          headers = ["Nama", "Jumlah", "Harga"]
          print(tb(data, headers=headers, tablefmt="fancy_grid"))
      else:
          print("Data tidak ditemukan.")
  
  def inorder_traversal(self, node, desc = False):
      if node != self.NIL:
        left_data = self.inorder_traversal(node.left, desc)
        current_data = [[node.nama, node.jumlah, node.harga]]
        right_data = self.inorder_traversal(node.right, desc)

        if desc:
            return right_data + current_data +left_data
        else:
            return left_data + current_data + right_data
      else :
        return []
      
  def display_data(self, desc = False):
    data = self.inorder_traversal(self.root, desc)
    if data:
      print(tb(data, headers=["Nama", "Jumlah", "Harga"], tablefmt="fancy_grid"))
    else:
       print("Tidak ada data hasil pertanian.")

  def delete(self, key):
    node_to_delete = self.search("nama", key)
    if node_to_delete == self.NIL:
      print("Barang tidak ditemukan")
      return
    self.delete_node(node_to_delete)
  
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
        self._fix_delete(x)

  def _transplant(self, u, v):
    if u.parent == self.NIL:
        self.root = v
    elif u == u.parent.left:
        u.parent.left = v
    else:
        u.parent.right = v
    v.parent = u.parent

  def _minimum(self, node):
    while node.left != self.NIL:
        node = node.left
    return node
  
  def _fix_delete(self, x):
    while x != self.root and x.color == 0:
      if x == x.parent.left:
        sibling = x.parent.right
        if sibling.color == 1:
          sibling.color = 0
          x.parent.color = 1
          self.left_rotate(x.parent)
          sibling = x.parent.right

        if sibling.left.color == 0 and sibling.right.color == 0:
          sibling.color = 1
          x = x.parent
        else:
          if sibling.right.color == 0:
              sibling.left.color = 0
              sibling.color = 1
              self.right_rotate(sibling)
              sibling = x.parent.right

          sibling.color = x.parent.color
          x.parent.color = 0
          sibling.right.color = 0
          self.left_rotate(x.parent)
          x = self.root
      else:
        sibling = x.parent.left
        if sibling.color == 1:
          sibling.color = 0
          x.parent.color = 1
          self.right_rotate(x.parent)
          sibling = x.parent.left
        if sibling.right.color == 0 and sibling.left.color == 0:
          sibling.color = 1
          x = x.parent
        else:
          if sibling.left.color == 0:
            sibling.right.color = 0
            sibling.color = 1
            self.left_rotate(sibling)
            sibling = x.parent.left
          sibling.color = x.parent.color
          x.parent.color = 0
          sibling.left.color = 0
          self.right_rotate(x.parent)
          x = self.root
    x.color = 0

  def save_to_file(self, filename = "hasilPertanian.csv"):
    data = self.inorder_traversal(self.root)
    with open(filename, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Nama", "Jumlah", "Harga"])
        csv_writer.writerows(data)
    
  def load_from_file(self, filename = "hasilPertanian.csv"):
    try:
      with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        data = [row for row in csv_reader]

      self.root = self.NIL
      for entry in data:
        key, jumlah, harga = entry
        self.insert(key, float(jumlah), float(harga))
        
    except FileNotFoundError:
       print("File tidak ditemukan")
        
  
