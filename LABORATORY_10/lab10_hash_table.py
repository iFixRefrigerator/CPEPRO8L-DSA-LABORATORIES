class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.buckets = [None] * capacity
        self.size = 0  # track number of stored entries (for load factor)

    def _hash(self, key):
        # Simple hash: sum of ASCII values modulo capacity.
        # Convert key to string to support ints/floats/strings uniformly.
        total = 0
        for ch in str(key):
            total += ord(ch)
        return total % self.capacity

    def put(self, key, value):
        index = self._hash(key)

        # Bucket is empty -> place new node
        if self.buckets[index] is None:
            self.buckets[index] = HashNode(key, value)
            self.size += 1
            return

        # Bucket occupied -> walk the chain
        current = self.buckets[index]
        while current:
            if current.key == key:
                current.value = value   # update existing key
                return
            if current.next is None:
                break
            current = current.next

        # Key not found in chain -> append new node (chaining)
        current.next = HashNode(key, value)
        self.size += 1

    def get(self, key):
        """Helper for demonstrating search efficiency."""
        index = self._hash(key)
        current = self.buckets[index]
        probes = 0
        while current:
            probes += 1
            if current.key == key:
                return current.value, probes
            current = current.next
        return None, probes

    def load_factor(self):
        return self.size / self.capacity

    def display(self):
        for idx in range(self.capacity):
            chain = []
            temp = self.buckets[idx]
            while temp:
                chain.append(f"[{temp.key}: {temp.value}]")
                temp = temp.next
            print(f"Bucket {idx}: " + " -> ".join(chain))


if __name__ == "__main__":
    ht = HashTable(5)
    ht.put("Alice", 25)
    ht.put("Bob", 30)
    ht.put("Charlie", 35)
    ht.display()
    print(f"\nLoad factor: {ht.load_factor():.2f}")
