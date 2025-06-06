# The rand7() API is already defined for you.
# def rand7():
# @return a random integer in the range 1 to 7

class Solution(object):
    def rand10(self):
        """
        :rtype: int
        """

        while True:
            first = (rand7() - 1) * 7 + (rand7()) 
            if first <= 40:
                return 1 + (first - 1) % 10
        
