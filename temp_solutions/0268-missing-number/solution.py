class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        nums.sort()
        n = len(nums)

        if 0 not in nums:
            return 0

        for i in range(1, n):
            if nums[i] - nums[i - 1] != 1:
                return nums[i - 1] + 1

        return n


