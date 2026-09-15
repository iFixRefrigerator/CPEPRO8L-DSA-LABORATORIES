def recursive_binary_search(arr, low, high, target):
    # Base Case: target is not in the array
    if low > high:
        return -1

    # Find middle index
    mid = (low + high) // 2

    # Base Case: target found
    if arr[mid] == target:
        return mid

    # If middle element is greater than target, search left half
    elif arr[mid] > target:
        return recursive_binary_search(arr, low, mid - 1, target)

    # Otherwise, search right half
    else:
        return recursive_binary_search(arr, mid + 1, high, target)


if __name__ == "__main__":
    data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    target_val = 23

    result = recursive_binary_search(data, 0, len(data) - 1, target_val)
    print(f"Element found at index: {result}")
