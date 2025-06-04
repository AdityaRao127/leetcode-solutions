from collections import Counter
class Solution:
    def firstUniqChar(self, s: str) -> int:
        if not s:
            return None
        

        counts = Counter(s)
        print(counts)

        for char in range(len(s)):
            if counts[s[char]] == 1:
                return char

        return -1
