class Solution:
    def hammingWeight(self, n: int) -> int:
        binary = bin(n)[2:]
        return (sum(1 for digit in binary if digit == '1'))
