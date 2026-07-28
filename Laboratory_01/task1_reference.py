# Task 1: Mutable references tracing
print("--- TASK 1: OBJECT ID COMPARISON ---")
list_a = [10, 20, 30]
list_b = list_a  # Copying the reference

print(f"Address of list_a (id): {id(list_a)}")
print(f"Address of list_b (id): {id(list_b)}")
print(f"Are list_a and list_b pointing to the same object? {list_a is list_b}")

# Mutating list_b
list_b.append(40)
print(f"\nAfter appending 40 to list_b:")
print(f"list_a: {list_a}")
print(f"list_b: {list_b}")

# New assignment to list_b
list_b = [100, 200]
print(f"\nAfter reassigning list_b to a new list:")
print(f"list_a: {list_a}")
print(f"list_b: {list_b}")
print(f"New address of list_b (id): {id(list_b)}")
print(f"Address of list_a (id): {id(list_a)}")
print(f"Are list_a and list_b now the same? {list_a is list_b}")
