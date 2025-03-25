class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        if n == 2:
            return 2 

        a, b= 1, 2
        for _ in range(3, n+1):
            temp = a + b
            a = b
            b=temp
        return b

    # "Start with 1 and 2, then slide the window summing previous two."
