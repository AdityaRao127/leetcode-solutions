class Solution(object):
    def arrangeCoins(self, n):
        """
        :type n: int
        :rtype: int
        """


        rows = 0
        i =1
        while(n>= i):
            n-= i
            rows += 1
            i+=1
        
        return rows


