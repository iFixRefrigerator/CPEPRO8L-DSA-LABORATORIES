class Stack:
    def __init__(self):
        self.items = []
    
    def is_empty(self):
        return len(self.items) == 0
    
    def push(self, item):
        # TODO: Append the item to the items list.
        self.items.append(item)
    
    def pop(self):
        # TODO: Pop and return the last item from the list.
        # Check if empty first and raise IndexError if so.
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack")
        return self.items.pop()
    
    def peek(self):
        return self.items[-1] if not self.is_empty() else None
    
    def size(self):
        return len(self.items)


def is_balanced(expression):
    stack = Stack()
    bracket_map = {')': '(', ']': '[', '}': '{'}
    
    for char in expression:
        # TODO: If char is an opening bracket, push it to stack.
        if char in '([{':
            stack.push(char)
        
        # If it is a closing bracket, pop from stack and check if it matches.
        elif char in ')]}':
            # If stack is empty or doesn't match, return False.
            if stack.is_empty():
                return False
            
            top_element = stack.pop()
            if bracket_map[char] != top_element:
                return False
    
    return stack.is_empty()


if __name__ == "__main__":
    # Test cases
    expr1 = "{{()}}"
    expr2 = "{{()}"  # Note: This is what the original code had (missing closing brace)
    expr3 = "{[()]}"
    expr4 = "([)]"
    expr5 = "((()))"
    
    print(f"Is '{expr1}' balanced? {is_balanced(expr1)}")  # Expected: True
    print(f"Is '{expr2}' balanced? {is_balanced(expr2)}")  # Expected: False
    print(f"Is '{expr3}' balanced? {is_balanced(expr3)}")  # Expected: True
    print(f"Is '{expr4}' balanced? {is_balanced(expr4)}")  # Expected: False
    print(f"Is '{expr5}' balanced? {is_balanced(expr5)}")  # Expected: True
