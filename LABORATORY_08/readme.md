# Lab 08: Binary Search Tree Operations

## Overview

A Binary Search Tree (BST) is a hierarchical, non-linear data structure. For any given node, all elements in its left subtree are smaller than the node's key, and all elements in its right subtree are greater. This property allows search operations to run in O(log n) average time.

## Objectives

1. Implement dynamic tree nodes with left and right child references.
2. Build insertion and lookup functions in a BST.
3. Implement Inorder, Preorder, and Postorder recursive tree traversals.

## Project Structure

```
lab8-bst/
├── lab8_bst.py        # Source code
├── README.md          # Documentation
└── images/
    └── bst_tree.JPG   # Test tree diagram
```

## Source Code

The script `lab8_bst.py` implements:

- `TreeNode` — a node with `key`, `left`, and `right` attributes.
- `BST` — the tree class with the following methods:
  - `insert(key)` — inserts a new key following BST rules.
  - `search(key)` — returns `True` if the key exists, otherwise `False`.
  - `inorder()` — returns keys in Left → Node → Right order.
  - `preorder()` — returns keys in Node → Left → Right order.
  - `postorder()` — returns keys in Left → Right → Node order.

## How to Run

```bash
python lab8_bst.py
```

## Execution & Output

### Test Tree

Inserted values: `[50, 30, 70, 20, 40, 60, 80]`

![BST Test Tree](images/bst_tree.png)

```
          50
        /    \
      30      70
     /  \    /  \
    20   40 60   80
```

### Console Output

```
Inserted values: [50, 30, 70, 20, 40, 60, 80]
Inorder  : [20, 30, 40, 50, 60, 70, 80]
Preorder : [50, 30, 20, 40, 70, 60, 80]
Postorder: [20, 40, 30, 60, 80, 70, 50]

Search 40: True
Search 90: False
```

## Report Analysis Questions

### Q1: Complete all traversals and write down the Preorder and Postorder outputs for the test tree.

Given the test tree built from inserting `[50, 30, 70, 20, 40, 60, 80]`:

- **Inorder (Left → Node → Right):** `[20, 30, 40, 50, 60, 70, 80]`
- **Preorder (Node → Left → Right):** `[50, 30, 20, 40, 70, 60, 80]`
- **Postorder (Left → Right → Node):** `[20, 40, 30, 60, 80, 70, 50]`

### Q2: Explain why the inorder traversal of a BST outputs items in sorted order.

In a Binary Search Tree, every node satisfies the BST property: all keys in its left subtree are smaller than the node's key, and all keys in its right subtree are greater. The inorder traversal visits nodes in the order **Left → Node → Right**.

Because the entire left (smaller) subtree is visited before the node, and the entire right (greater) subtree is visited after, the keys are emitted in ascending order. Since this rule holds recursively at every node, the final output is fully sorted.

## Author

**Robles, John Vincent M.**\
BSCOME - 2  
29 SEPTEMBER 2026
