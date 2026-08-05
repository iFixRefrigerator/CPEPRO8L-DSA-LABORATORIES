# Lab 4: Doubly & Circular Linked Lists

## Objectives
- To implement a Doubly Linked List using next and prev pointers.
- To create a Circular Singly Linked List and verify that the tail node links back to the head node.
- To understand the different traversal termination conditions used by linear and circular linked lists.

## Source Code
The Python source code for this laboratory activity is contained in:
[`lab4_doubly_circular.py`](./lab4_doubly_circular.py)

The program includes the following classes:
```
- DoubleNode
- DoublyLinkedList
- Node
- CircularSinglyLinkedList
```

## Execution Output
```
--- Testing Doubly Linked List ---
None <-> 10 <-> 5 <-> None

--- Testing Circular Linked List ---
100 -> 200 -> 300 -> (loops to 100)
```

## Execution and Output Analysis
### Doubly Linked List
The values 5 and 10 are inserted at the head of the list.
The value 5 is inserted first:
```
None <-> 5 <-> None
```
The value 10 is then inserted at the head:
```
None <-> 10 <-> 5 <-> None
```
The output demonstrates that the new node becomes the head of the list and that the nodes are correctly connected using the next and prev references.

### Circular Singly Linked List
The values 100, 200, and 300 are inserted at the tail of the list.
The resulting circular structure is:
```
100 -> 200 -> 300
 ^                 |
 |_________________|
```
The final node, containing 300, points back to the head node, containing 100. The program displays each node once and indicates that the list loops back to the first value.

## Report Analysis Question
Explain the termination condition in a loop traversal of a Circular Linked List to prevent infinite loops.
- In a Circular Linked List, the last node does not point to None. Instead, the last node points back to the head node. Because of this structure, using a condition such as while temp is not None would cause the traversal to continue indefinitely.
To prevent an infinite loop, the traversal must stop when the current pointer returns to the head node. The program begins at the head and visits each node. After moving to the next node, it checks whether the pointer is equal to the head.
The termination condition is:
```
if temp == self.head:
    break
```
This condition ensures that all nodes are visited only once. When the pointer reaches the head again, the program recognizes that it has completed one full traversal and terminates the loop.
