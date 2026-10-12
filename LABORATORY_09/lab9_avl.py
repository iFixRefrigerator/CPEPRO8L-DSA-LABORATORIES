class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_right(self, y):
        """Right rotation (LL case). Returns the new root."""
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights (y first, then x)
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    def rotate_left(self, x):
        """Left rotation (RR case). Returns the new root."""
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights (x first, then y)
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, root, key):
        # 1. Standard BST insertion
        if not root:
            return AVLNode(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            return root  # duplicate keys not allowed

        # 2. Update height of this ancestor node
        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))

        # 3. Get the balance factor
        balance = self.get_balance(root)

        # 4. Balance the tree if needed
        # Case 1: Left Left (LL)
        if balance > 1 and key < root.left.key:
            return self.rotate_right(root)

        # Case 2: Right Right (RR)
        if balance < -1 and key > root.right.key:
            return self.rotate_left(root)

        # Case 3: Left Right (LR)
        if balance > 1 and key > root.left.key:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # Case 4: Right Left (RL)
        if balance < -1 and key < root.right.key:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    # ---------- Helpers for demonstration / tracing ----------
    def pre_order(self, root, depth=0, prefix="Root: "):
        if not root:
            return
        print(" " * (depth * 4) + prefix + str(root.key)
              + f" (h={root.height}, bf={self.get_balance(root)})")
        if root.left or root.right:
            if root.left:
                self.pre_order(root.left, depth + 1, "L--- ")
            else:
                print(" " * ((depth + 1) * 4) + "L--- None")
            if root.right:
                self.pre_order(root.right, depth + 1, "R--- ")
            else:
                print(" " * ((depth + 1) * 4) + "R--- None")


# ---------- Demonstration ----------
if __name__ == "__main__":
    tree = AVLTree()
    root = None

    keys = [10, 20, 30]
    print("=== Inserting keys [10, 20, 30] ===\n")
    for k in keys:
        print(f"--- After inserting {k} ---")
        root = tree.insert(root, k)
        tree.pre_order(root)
        print(f"Current root: {root.key}\n")
