# Laboratory Activity 03: Singly Linked List CRUD

---

## 1. Objectives
- Construct custom `Node` and `SinglyLinkedList` classes.
- Implement insertion at the head, tail, and specific values.
- Manage list nodes and pointers cleanly without losing references.

---

## 2. Execution & Output

**Code:** [`lab3_singly_linked_list.py`](lab3_singly_linked_list.py)

**Console Output:**
```
20 -> 10 -> 30 -> None
20 -> 30 -> None
Is 30 in list? True
```

---

## 3. Analysis Questions

**Question 1: Trace the pointers step-by-step when deleting the middle node (value 10).**

Initial list: `20 (head) -> 10 -> 30 -> None`

1. Start at `head` (node with value 20).
2. Check if `head.data == 10`? No.
3. Move to the next node using `temp.next`. 
4. Now `temp` is at node 20. Check `temp.next.data`: 
   - `temp.next` is node 10.
   - `10 == 10` (target found!).
5. Update the pointer: `temp.next = temp.next.next`.
   - This means node 20 now points directly to node 30.
6. Node 10 is now **unlinked** from the list and will be garbage collected.
7. Final list: `20 -> 30 -> None`

---

## 4. Conclusions
Singly Linked Lists are efficient for dynamic insertion and deletion at the head (O(1)), but searching and tail insertion require O(n) traversal because nodes are not stored contiguously. Pointer management is critical—forgetting to update the `next` reference can break the entire chain.

---

## Files Included
- `lab3_singly_linked_list.py` – Source code
- `README.md` – Lab report
