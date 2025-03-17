class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""
        
        prefix = strs[0]

        for words in strs[1:]:
            while not words.startswith(prefix):
                prefix = prefix[:-1]

        return prefix
        

