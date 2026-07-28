import ctypes

class DynamicArray:
    def __init__(self):
        self.size = 0          # number of actual elements
        self.capacity = 1      # initial capacity
        self.array = self._make_array(self.capacity)

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        # TODO: Check if index is valid
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        return self.array[index]

    def append(self, element):
        # TODO: Check if size == capacity, then resize
        if self.size == self.capacity:
            self._resize(2 * self.capacity)  # double the capacity
        
        # Place element at current size, then increment size
        self.array[self.size] = element
        self.size += 1

    def _resize(self, new_capacity):
        # TODO: Print capacity change trace
        print(f"Resizing from {self.capacity} to {new_capacity}")
        
        # 1. Make a new array with new_capacity
        new_array = self._make_array(new_capacity)
        
        # 2. Copy elements from old array to new array
        for i in range(self.size):
            new_array[i] = self.array[i]
        
        # 3. Reassign self.array and self.capacity
        self.array = new_array
        self.capacity = new_capacity

    def _make_array(self, new_capacity):
        # Returns a ctypes array of the given capacity
        return (new_capacity * ctypes.py_object)()


# --- TESTING SCRIPT ---
if __name__ == "__main__":
    arr = DynamicArray()
    print("--- Starting append loop ---")
    for i in range(10):
        arr.append(i)
        print(f"Appending {i} | Size: {len(arr)} | Capacity: {arr.capacity} | Element at index {i}: {arr[i]}")
