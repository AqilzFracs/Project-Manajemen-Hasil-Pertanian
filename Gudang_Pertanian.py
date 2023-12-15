from tabulate import tabulate
import csv

class RedBlackTreeNode:
    def __init__(self, key, value ,color, left=None, right=None, parent=None):
        self.key = key
        self.value = value
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent


class RedBlackTree:
    def __init__(self):
        self.NIL = RedBlackTreeNode(None, None, 0)
        self.root = self.NIL

    def insert(self, key, value):
        new_node = RedBlackTreeNode(key, value, 1, self.NIL, self.NIL, self.NIL)
        self._insert_node(self.root, new_node)
        self._fix_insert(new_node)

    def _insert_node(self, root, new_node):
        if root == self.NIL:
            self.root = new_node
        elif new_node.key < root.key:
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


    def search_key(self, key):
        result_list = []
        self.search_helper_key(self.root, key, result_list)
        return result_list
    
    def search_value(self, value):
        result_list = []
        self.search_helper_value(self.root, value, result_list)
        return result_list

    def search_helper_key(self, node, key, result_list):
        if node != self.NIL:
            self.search_helper_key(node.left, key, result_list)
            if key.lower() in node.key.lower():  # Case-insensitive partial match
                result_list.append(node)
            self.search_helper_key(node.right, key, result_list)
        
    def search_helper_value(self, node, value, result_list):
        if node != self.NIL:
            self.search_helper_value(node.left, value, result_list)
            if node.value == value:
                result_list.append(node)
            self.search_helper_value(node.right, value, result_list)

    def display_data(self, descending = False):
        if descending:
            data = self.inorder_traversal_descending(self.root)
            if data:
                # print("Data in-order traversal:")
                tmp_data = []
                for node in data:
                    tmp = [node.key, node.value]
                    tmp_data.append(tmp)

                print(tabulate(tmp_data, headers=["Nama", "Jumlah"], tablefmt="fancy_grid"))
                
            else:
                print("Pohon kosong.")
        else:
            data = self.inorder_traversal(self.root)
            if data:
                # print("Data in-order traversal:")
                tmp_data = []
                for node in data:
                    tmp = [node.key, node.value]
                    tmp_data.append(tmp)

                print(tabulate(tmp_data, headers=["Nama", "Jumlah"], tablefmt="fancy_grid"))
                
            else:
                print("Pohon kosong.")

    def inorder_traversal(self, node):
        if node != self.NIL:
            left_data = self.inorder_traversal(node.left)
            current_data = [node]
            right_data = self.inorder_traversal(node.right)
            return left_data + current_data + right_data
        else:
            return []
    
    def inorder_traversal_descending(self, node):
        if node != self.NIL:
            right_data = self.inorder_traversal_descending(node.right)
            current_data = [node]
            left_data = self.inorder_traversal_descending(node.left)

            return right_data + current_data + left_data
        else:
            return []
        
    def delete(self, key):
        node = self.search_key(key)
        if node != self.NIL:
            self.delete_node(node)

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

    def minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node
    
    def transplant(self, u, v):
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def edit(self, old_key, new_key, new_value):
        node_to_edit = self.search_key(old_key)
        if node_to_edit != self.NIL:
            node_to_edit.key = new_key
            node_to_edit.value = new_value
            print("Data berhasil diperbarui.")
        else:
            print("Data tidak ditemukan.")

    def save_to_file(self, filename="hasilPertanian.csv"):
        data = self.inorder_traversal(self.root)
        if data:
            with open(filename, 'w', encoding='utf-8') as file:
                for node in data:
                    line = f"{node.key},{node.value}\n"
                    file.write(line)
                # print(f'Data has been saved to {filename}')
