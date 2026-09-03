class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.head = 0
        self.tail = 0
        self.size = 0

    def is_full(self):
        return self.size == self.capacity

    def is_empty(self):
        return self.size == 0

    def enqueue(self, item):
        # TODO: If full, print overflow warning and return False.
        if self.is_full():
            print(f"Overflow Warning: Queue is full. Cannot enqueue {item}")
            return False
        
        # Otherwise, insert item at tail, increment size, and update tail circularly.
        self.queue[self.tail] = item
        self.size += 1
        self.tail = (self.tail + 1) % self.capacity
        return True

    def dequeue(self):
        # TODO: If empty, print underflow warning and return None.
        if self.is_empty():
            print("Underflow Warning: Queue is empty. Cannot dequeue.")
            return None
        
        # Otherwise, retrieve head item, set position to None, decrement size, and update head circularly.
        item = self.queue[self.head]
        self.queue[self.head] = None
        self.size -= 1
        self.head = (self.head + 1) % self.capacity
        return item

    def display(self):
        print(f"Queue array: {self.queue} | Head: {self.head} | Tail: {self.tail}")


if __name__ == "__main__":
    cq = CircularQueue(5)
    cq.enqueue(1)
    cq.enqueue(2)
    cq.enqueue(3)
    print(f"Dequeued: {cq.dequeue()}")  # Expected: Dequeued: 1
    cq.enqueue(4)
    cq.display()
