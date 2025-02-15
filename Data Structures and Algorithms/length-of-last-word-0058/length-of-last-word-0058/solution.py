class Solution(object):
    def lengthOfLastWord(self, s):
        """
        :type s: str
        :rtype: int
        """
        word = s.strip()
        word = word.split(" ")
        #print(len(word[-1]))
        return len(word[-1])


