class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        if(len(prices) == 1):
            return 0
        
        if (len(prices) == 2):
            return (prices[1] - prices[0]) if (prices[1] - prices[0]) > 0 else 0
    
        min = prices[0]
        max = 0
        for i in range(len(prices)):
            if(prices[i] < min):
                min = prices[i]

            if((prices[i] - min) > max):
                max = prices[i] - min
                print(max)
        return max

"""
        max = 0
        for i in range(len(prices)-1):
            for j in range(i, len(prices)):
                if((prices[j] - prices[i]) > max):
                    max = prices[j] - prices[i]

        
        return abs(max)
"""





