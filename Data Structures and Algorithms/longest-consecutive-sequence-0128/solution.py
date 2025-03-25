class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        
        seen = []
        longest = 1
        current =1

        if not nums:
            return 0

        nums.sort()

        for i in range(1, len(nums)):
            if nums[i] ==nums[i-1]:
                continue
            if nums[i] == nums[i-1] + 1:
                current+= 1
            else:
                longest = max(current, longest)
                current = 1
            
        return max(current, longest)
    
    # Skip duplicates during consecutive checks by comparing current and previous; if equal, continue the loop without breaking or advancing the streak count.
