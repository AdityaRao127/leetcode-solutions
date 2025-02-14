class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        longest_prefix = ""
        for i in range(len(strs[0])):
            prefix = strs[0][:i+1]
            if all(word.startswith(prefix) for word in strs):
                longest_prefix = prefix
            else:
                break
        return longest_prefix
