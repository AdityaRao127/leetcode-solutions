class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
    
        if(nums[-1] < target):
            return len(nums)
        
        if(nums[0] > target):
            return 0

        low = 0
        high = len(nums) -1

        while low <= high:
            mid = (low + high) // 2
            

            if(nums[mid] == target):
                return mid
            elif (nums[mid] < target):
                low = mid+1
            else:
                high = mid -1
        
        return low

