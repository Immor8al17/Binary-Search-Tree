import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None
        self.positions = {}

    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._insert(self.root, value)

    def _insert(self, current_node, value):
        if value < current_node.value:
            if current_node.left is None:
                current_node.left = Node(value)
            else:
                self._insert(current_node.left, value)
        else:
            if current_node.right is None:
                current_node.right = Node(value)
            else:
                self._insert(current_node.right, value)

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if not node:
            return node

        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left

            successor = self._min_value_node(node.right)
            node.value = successor.value
            node.right = self._delete(node.right, successor.value)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def calculate_positions(self):
        self.positions = {}
        if self.root:
            self._calculate_positions(self.root, 400, 50, 200)

    def _calculate_positions(self, node, x, y, dx):
        if not node:
            return
        self.positions[node] = (x, y)
        if node.left:
            self._calculate_positions(node.left, x - dx, y + 80, dx // 2)
        if node.right:
            self._calculate_positions(node.right, x + dx, y + 80, dx // 2)

    def search(self, node, value):
        if not node:
            return None
        if value == node.value:
            return node
        if value < node.value:
            return self.search(node.left, value)
        return self.search(node.right, value)

    def inorder_traversal(self, node):
        if node:
            yield from self.inorder_traversal(node.left)
            yield node
            yield from self.inorder_traversal(node.right)

    def preorder_traversal(self, node):
        if node:
            yield node
            yield from self.preorder_traversal(node.left)
            yield from self.preorder_traversal(node.right)

    def postorder_traversal(self, node):
        if node:
            yield from self.postorder_traversal(node.left)
            yield from self.postorder_traversal(node.right)
            yield node


class TreeVisualizer(ttk.Window):
    def __init__(self):
        super().__init__(themename="solar")

        self.title("Binary Tree Visualizer")
        self.geometry("800x600")

        self.tree = BinaryTree()
        self.canvas = ttk.Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack()

        self.input_field = ttk.Entry(self, width=20)
        self.input_field.pack(pady=5)

        self.insert_button = ttk.Button(self, text="Insert", command=self.insert_node, bootstyle=SUCCESS)
        self.insert_button.pack(pady=5)

        self.delete_button = ttk.Button(self, text="Delete", command=self.delete_node, bootstyle=DANGER)
        self.delete_button.pack(pady=5)

        self.search_button = ttk.Button(self, text="Search", command=self.search_node, bootstyle=INFO)
        self.search_button.pack(pady=5)

        self.inorder_button = ttk.Button(self, text="Inorder Traversal", command=self.visualize_inorder, bootstyle=SECONDARY)
        self.inorder_button.pack(pady=5)

        self.preorder_button = ttk.Button(self, text="Preorder Traversal", command=self.visualize_preorder, bootstyle=PRIMARY)
        self.preorder_button.pack(pady=5)

        self.postorder_button = ttk.Button(self, text="Postorder Traversal", command=self.visualize_postorder, bootstyle=WARNING)
        self.postorder_button.pack(pady=5)

        self.update_canvas()

    def insert_node(self):
        value = self.input_field.get()
        if value.strip() == "":
            messagebox.showerror("Input Error", "Please enter a value to insert.")
            return

        try:
            value = int(value)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer value.")
            return

        self.tree.insert(value)
        self.input_field.delete(0, ttk.END)
        self.update_canvas()

    def delete_node(self):
        value = self.input_field.get()
        if value.strip() == "":
            messagebox.showerror("Input Error", "Please enter a value to delete.")
            return

        try:
            value = int(value)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer value.")
            return

        self.tree.delete(value)
        self.input_field.delete(0, ttk.END)
        self.update_canvas()

    def search_node(self):
        value = self.input_field.get()
        if value.strip() == "":
            messagebox.showerror("Input Error", "Please enter a value to search.")
            return

        try:
            value = int(value)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer value.")
            return

        target_node = self.tree.search(self.tree.root, value)
        if target_node:
            x, y = self.tree.positions[target_node]
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="red")
            messagebox.showinfo("Search Result", f"Value {value} found in the tree.")
        else:
            messagebox.showinfo("Search Result", f"Value {value} not found in the tree.")

    def update_canvas(self):
        self.canvas.delete("all")
        self.tree.calculate_positions()

        for node, (x, y) in self.tree.positions.items():
            if node.left:
                lx, ly = self.tree.positions[node.left]
                self.canvas.create_line(x, y + 20, lx, ly - 20, fill="white")
            if node.right:
                rx, ry = self.tree.positions[node.right]
                self.canvas.create_line(x, y + 20, rx, ry - 20, fill="white")
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightgreen")
            self.canvas.create_text(x, y, text=str(node.value))

    def reset_colors(self):
        for node, (x, y) in self.tree.positions.items():
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightgreen")
            self.canvas.create_text(x, y, text=str(node.value))

    def visualize_traversal(self, traversal_generator):
        def step():
            try:
                node = next(traversal)
                x, y = self.tree.positions[node]
                self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="yellow")
                self.after(1000, step)
            except StopIteration:
                return

        traversal = traversal_generator
        step()

    def visualize_inorder(self):
        if not self.tree.root:
            messagebox.showinfo("Tree Info", "The tree is empty. Nothing to traverse.")
            return
        self.reset_colors()
        self.visualize_traversal(self.tree.inorder_traversal(self.tree.root))

    def visualize_preorder(self):
        if not self.tree.root:
            messagebox.showinfo("Tree Info", "The tree is empty. Nothing to traverse.")
            return
        self.reset_colors()
        self.visualize_traversal(self.tree.preorder_traversal(self.tree.root))

    def visualize_postorder(self):
        if not self.tree.root:
            messagebox.showinfo("Tree Info", "The tree is empty. Nothing to traverse.")
            return
        self.reset_colors()
        self.visualize_traversal(self.tree.postorder_traversal(self.tree.root))


if __name__ == "__main__":
    app = TreeVisualizer()
    app.mainloop()
