class Solution:
    def reverseBits(self, n: int) -> int:
        reverse = bin(n)[2:].zfill(32)[::-1]
        return int(reverse, 2)
