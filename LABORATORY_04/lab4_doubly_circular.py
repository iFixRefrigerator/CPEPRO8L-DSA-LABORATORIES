class DoubleNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
    
    def insert_head(self, data):
        new_node = DoubleNode(data)
        if self.head is None:
            self.head = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
    
    def display_forward(self):
        temp = self.head
        elements = []
        while temp:
            elements.append(str(temp.data))
            temp = temp.next
        print("None <-> " + " <-> ".join(elements) + " <-> None")

class CircularSinglyLinkedList:
    def __init__(self):
        self.head = None
    
    def insert_tail(self, data):
        new_node = DoubleNode(data)  # Using DoubleNode but only next pointer matters
        if self.head is None:
            self.head = new_node
            new_node.next = self.head  # Circular link to itself
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head
    
    def display(self):
        if self.head is None:
            print("List is empty")
            return
        temp = self.head
        elements = []
        while True:
            elements.append(str(temp.data))
            temp = temp.next
            if temp == self.head:  # Termination condition
                break
        print(" -> ".join(elements) + " -> (loops to " + str(self.head.data) + ")")

if __name__ == "__main__":
    print("--- Testing Doubly Linked List ---")
    dll = DoublyLinkedList()
    dll.insert_head(5)
    dll.insert_head(10)
    dll.display_forward()  # Expected: None <- > 10 <- > 5 <- > None
    
    print("\n--- Testing Circular Linked List ---")
    cll = CircularSinglyLinkedList()
    cll.insert_tail(100)
    cll.insert_tail(200)
    cll.insert_tail(300)
    cll.display()  # Expected: 100 -> 200 -> 300 -> (loops to 100)
