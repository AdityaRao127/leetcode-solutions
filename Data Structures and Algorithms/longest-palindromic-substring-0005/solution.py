class Solution:
    def longestPalindrome(self, s: str) -> str:
        def expand(left: int, right: int) -> str:
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return s[left+1:right]

        longest = ""
        for i in range(len(s)):
            # Odd length
            p1 = expand(i, i)
            # Even length
            p2 = expand(i, i + 1)

            if len(p1) > len(longest):
                longest = p1
            if len(p2) > len(longest):
                longest = p2

        return longest

"""


class Solution:
    def longestPalindrome(self, s: str) -> str:
        if s == s[::-1]:
            return s
        
        if len(s) == 2:
            return s if s[0] == s[1] else s[0]
        
        n = len(s)
        longest = s[0]
        
        for left in range(n):
            right = n
            while right > left:
                substr = s[left:right]
                if substr == substr[::-1] and len(substr) > len(longest):
                    longest = substr
                right -= 1
        
        return longest
"""
