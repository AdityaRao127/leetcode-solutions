class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len((t)):
            return False
        
        seen = {}
        for char in s:
            seen[char] = seen.get(char, 0) + 1
        
        print(seen)
        compare = {}
        for char in t:
            compare[char] =compare.get(char, 0)+1

        if compare == seen:
            return True

        return False
        
