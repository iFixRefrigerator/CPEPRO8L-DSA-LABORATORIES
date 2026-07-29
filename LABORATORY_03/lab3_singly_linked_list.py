class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_head(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_tail(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def delete_value(self, target):
        if self.head is None:
            return False
        
        # If head is the target
        if self.head.data == target:
            self.head = self.head.next
            return True
        
        current = self.head
        while current.next:
            if current.next.data == target:
                current.next = current.next.next
                return True
            current = current.next
        return False

    def search(self, target):
        current = self.head
        while current:
            if current.data == target:
                return True
            current = current.next
        return False

    def display(self):
        temp = self.head
        elements = []
        while temp:
            elements.append(str(temp.data))
            temp = temp.next
        print(" -> ".join(elements) + " -> None")

if __name__ == "__main__":
    sll = SinglyLinkedList()
    sll.insert_head(10)
    sll.insert_head(20)
    sll.insert_tail(30)
    sll.display()  # Expected: 20 -> 10 -> 30 -> None
    
    sll.delete_value(10)
    sll.display()  # Expected: 20 -> 30 -> None
    
    print(f"Is 30 in list? {sll.search(30)}")  # Expected: True
