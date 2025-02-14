class Solution(object):
    def strStr(self, haystack, needle):
        """
        :type haystack: str
        :type needle: str
        :rtype: int
        """

        length = len(needle)
        i =0
        for i in range(len(haystack)):
            print(haystack[i:i+length:])
            if needle == haystack[i:i+length]:
                return i
            else:
                i+=length
        
        return -1

