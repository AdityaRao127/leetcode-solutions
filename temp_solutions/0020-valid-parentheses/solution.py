class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        mapping = {')' : '(', '}': '{', ']':'['}

        for char in s:
            if char not in mapping:
                stack.append(char)
                continue
            if not stack or mapping[char] != stack.pop():
                return False

        return not stack

