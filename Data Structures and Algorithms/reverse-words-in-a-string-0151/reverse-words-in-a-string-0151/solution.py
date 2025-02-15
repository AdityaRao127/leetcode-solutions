class Solution(object):
    def reverseWords(self, s):
        """
        :type s: str
        :rtype: str
        """

        s = s.strip()
        print(s)
        words = s.split()
        print(words)
        words.reverse()
        print(words)
        return " ".join(words)

        
