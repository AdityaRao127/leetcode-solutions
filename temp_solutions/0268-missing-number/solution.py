class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        nums.sort()
        n = len(nums)

        if 0 not in nums:
            return 0

        for i in range(n-1):
            if (nums[i] + 1 )!= nums[i+1]:
                return i+1
        
        return nums[-1] +1
