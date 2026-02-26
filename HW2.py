import csv

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class HomeWork2:

    # Problem 1: Construct an expression tree (Binary Tree) from a postfix expression
    # input -> list of strings (e.g., ["3","4","+","2","*"])
    # this is parsed from p1_construct_tree.csv (check it out for clarification)
    #
    # there are no duplicate numeric values in the input
    # support basic operators: +, -, *, /
    #
    # output -> the root node of the expression tree.
    # Example postfix: [3,4,+,2,*]
    # Tree should be:
    #         *
    #        / \
    #       +   2
    #      / \
    #     3   4

    def constructBinaryTree(self, input) -> TreeNode:
        operators = {"+", "-", "*", "/"}
        stack = []

        # Edge-case handling (Problem 4):
        # If input list is empty, we cannot construct a tree.
        if input is None or len(input) == 0:
            raise ValueError("Empty postfix expression (cannot construct tree)")

        for token in input:
            token = token.strip()

            # Edge-case handling (Problem 4):
            # Invalid/empty token
            if token == "":
                raise ValueError("Invalid token: empty string")

            # Operand (number)
            if token not in operators:
                # Edge-case handling (Problem 4):
                # Ensure operand is actually an integer (supports negative numbers)
                try:
                    int(token)
                except ValueError:
                    raise ValueError(f"Invalid token (not an integer): {token}")

                stack.append(TreeNode(token))

            # Operator
            else:
                # Edge-case handling (Problem 4):
                # For an operator, we must have at least TWO operands on stack
                if len(stack) < 2:
                    raise ValueError("Malformed postfix expression: insufficient operands for operator")

                # operator: pop right then left
                right = stack.pop()
                left = stack.pop()

                node = TreeNode(token, left, right)
                stack.append(node)

        # Edge-case handling (Problem 4):
        # After processing, there must be EXACTLY one node (the root).
        if len(stack) != 1:
            raise ValueError("Malformed postfix expression: too many operands (extra nodes remain)")

        return stack.pop()


    # Problem 2.1: Use pre-order traversal (root, left, right) to generate prefix notation
    # return an array of elements of a prefix expression
    # expected output for the tree from problem 1 is ["*","+","3","4","2"]
    def prefixNotationPrint(self, head: TreeNode) -> list:
        result = []

        def preorder(node):
            if node is None:
                return
            result.append(str(node.val))   # visit root
            preorder(node.left)            # go left
            preorder(node.right)           # go right

        preorder(head)
        return result


    # Problem 2.2: Use in-order traversal (left, root, right) for infix notation with appropriate parentheses.
    # return an array of elements of an infix expression
    # expected output for the tree from problem 1 is ["(", "(", "3", "+", "4", ")", "*", "2", ")"]
    #
    # don't forget to add parentheses to maintain correct sequence
    # even the outermost expression should be wrapped
    # treat parentheses as individual elements in the returned list
    def infixNotationPrint(self, head: TreeNode) -> list:
        result = []

        def is_leaf(node):
            return node is not None and node.left is None and node.right is None

        def inorder_with_parens(node):
            if node is None:
                return

            # leaf: just output the value
            if is_leaf(node):
                result.append(str(node.val))
                return

            # internal node: ( left op right )
            result.append("(")
            inorder_with_parens(node.left)
            result.append(str(node.val))
            inorder_with_parens(node.right)
            result.append(")")

        inorder_with_parens(head)
        return result


    # Problem 2.3: Use post-order traversal (left, right, root) to generate postfix notation.
    # return an array of elements of a postfix expression
    # expected output for the tree from problem 1 is ["3","4","+","2","*"]
    def postfixNotationPrint(self, head: TreeNode) -> list:
        result = []

        def postorder(node):
            if node is None:
                return
            postorder(node.left)           # left
            postorder(node.right)          # right
            result.append(str(node.val))   # root

        postorder(head)
        return result


class Stack:
    # Implement your stack using either an array or a list
    # manually managing the "top" pointer (Stack ADT)

    def __init__(self):
        self.data = []
        self.top = -1

    def is_empty(self):
        return self.top == -1

    def push(self, item):
        self.data.append(item)
        self.top += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        item = self.data[self.top]
        self.data.pop()
        self.top -= 1
        return item

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self.data[self.top]

    # Problem 3: Evaluate a postfix expression using Stack and return integer value
    #
    # ---------------- Problem 4 (Edge Cases) Notes ----------------
    # This method handles:
    # 1) Empty postfix expression -> ValueError
    # 2) Malformed postfix:
    #    - insufficient operands for an operator -> ValueError
    #    - too many operands left at end -> ValueError
    # 3) Division by zero -> ZeroDivisionError (caught in provided main)
    # 4) Invalid tokens:
    #    - non-numeric operands -> ValueError
    #    - unsupported operators -> ValueError
    # 5) Very large numbers/results:
    #    - Python ints do not overflow (arbitrary precision), so it still works correctly.
    # 6) Negative numbers:
    #    - int(token) supports "-3" naturally, so negative operands are supported.
    #
    # DO NOT USE eval()
    def evaluatePostfix(self, exp: str) -> int:
        operators = {"+", "-", "*", "/"}

        # Edge case: empty expression ("" or just spaces)
        if exp is None or exp.strip() == "":
            raise ValueError("Empty postfix expression")

        tokens = exp.split()

        for token in tokens:
            # Operator token
            if token in operators:
                # Edge case: insufficient operands
                # Need at least 2 values on the stack to apply a binary operator
                if self.top < 1:
                    raise ValueError("Malformed postfix expression: insufficient operands")

                b = self.pop()  # right operand
                a = self.pop()  # left operand

                if token == "+":
                    self.push(a + b)
                elif token == "-":
                    self.push(a - b)
                elif token == "*":
                    self.push(a * b)
                elif token == "/":
                    # Edge case: division by zero
                    if b == 0:
                        raise ZeroDivisionError("division by zero")
                    # integer division behavior (truncate toward 0)
                    self.push(int(a / b))

            # Operand token (must be integer)
            else:
                # Edge case: invalid token (not an integer)
                try:
                    num = int(token)  # supports negative numbers too
                except ValueError:
                    raise ValueError(f"Invalid token (not an integer): {token}")

                self.push(num)

        # Edge case: too many operands (stack should end with exactly 1 value)
        if self.top != 0:
            raise ValueError("Malformed postfix expression: too many operands")

        return self.pop()


# ---------------- Optional Edge Case Tests (Problem 4) ----------------

def run_edge_case_tests():
    tests = [
        # Empty
        ("", "ValueError"),
        ("   ", "ValueError"),

        # Malformed: insufficient operands
        ("+", "ValueError"),
        ("5 +", "ValueError"),
        ("2 3 + *", "ValueError"),

        # Malformed: too many operands
        ("3 4 5 +", "ValueError"),
        ("10 20", "ValueError"),

        # Division by zero
        ("5 0 /", "ZeroDivisionError"),
        ("10 2 2 - /", "ZeroDivisionError"),

        # Invalid tokens
        ("3 a +", "ValueError"),
        ("4 2 ^", "ValueError"),

        # Large numbers (Python handles big ints)
        ("999999999999999999 999999999999999999 *", "OK"),

        # Negative numbers
        ("5 -3 *", "OK"),
        ("-10 3 /", "OK"),
    ]

    for expr, expected in tests:
        s = Stack()
        try:
            val = s.evaluatePostfix(expr)
            if expected == "OK":
                print(f"PASS: {expr!r} => {val}")
            else:
                print(f"FAIL: {expr!r} expected {expected} but got value {val}")
        except ZeroDivisionError:
            print("PASS" if expected == "ZeroDivisionError" else "FAIL", f": {expr!r} raised ZeroDivisionError")
        except ValueError:
            print("PASS" if expected == "ValueError" else "FAIL", f": {expr!r} raised ValueError")


# Main Function. Do not edit the code below
if __name__ == "__main__":
    homework2 = HomeWork2()

    print("\nRUNNING TEST CASES FOR PROBLEM 1")
    testcases = []
    try:
        with open('p1_construct_tree.csv', 'r') as f:
            testcases = list(csv.reader(f))
    except FileNotFoundError:
        print("p1_construct_tree.csv not found")

    for i, (postfix_input,) in enumerate(testcases, 1):
        postfix = postfix_input.split(",")

        root = homework2.constructBinaryTree(postfix)
        output = homework2.postfixNotationPrint(root)

        assert output == postfix, f"P1 Test {i} failed: tree structure incorrect"
        print(f"P1 Test {i} passed")

    print("\nRUNNING TEST CASES FOR PROBLEM 2")
    testcases = []
    with open('p2_traversals.csv', 'r') as f:
        testcases = list(csv.reader(f))

    for i, row in enumerate(testcases, 1):
        postfix_input, exp_pre, exp_in, exp_post = row
        postfix = postfix_input.split(",")

        root = homework2.constructBinaryTree(postfix)

        assert homework2.prefixNotationPrint(root) == exp_pre.split(","), f"P2-{i} prefix failed"
        assert homework2.infixNotationPrint(root) == exp_in.split(","), f"P2-{i} infix failed"
        assert homework2.postfixNotationPrint(root) == exp_post.split(","), f"P2-{i} postfix failed"

        print(f"P2 Test {i} passed")

    print("\nRUNNING TEST CASES FOR PROBLEM 3")
    testcases = []
    try:
        with open('p3_eval_postfix.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                testcases.append(row)
    except FileNotFoundError:
        print("p3_eval_postfix.csv not found")

    for idx, row in enumerate(testcases, start=1):
        expr, expected = row

        try:
            s = Stack()
            result = s.evaluatePostfix(expr)
            if expected == "DIVZERO":
                print(f"Test {idx} failed (expected division by zero)")
            else:
                expected = int(expected)
                assert result == expected, f"Test {idx} failed: {result} != {expected}"
                print(f"Test case {idx} passed")

        except ZeroDivisionError:
            assert expected == "DIVZERO", f"Test {idx} unexpected division by zero"
            print(f"Test case {idx} passed (division by zero handled)")