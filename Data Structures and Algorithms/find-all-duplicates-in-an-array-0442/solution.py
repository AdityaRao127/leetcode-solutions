class Solution:
    def findDuplicates(self, nums: List[int]) -> List[int]:
        numCounts = {}

        for i in range(len(nums)):
            if nums[i] not in numCounts:
                numCounts[nums[i]] = 1
            
            else:
                numCounts[nums[i]] += 1
        
        print(numCounts)

        sorted_dict_values_desc = sorted(numCounts.items(), key=lambda item: item[1], reverse=True)

        return [num for num, count in numCounts.items() if count == 2]

"""
class Solution:
    def findDuplicates(self, nums: List[int]) -> List[int]:
        res = []
        for num in nums:
            n = abs(num)
            if nums[n - 1] < 0:
                res.append(n)
            nums[n - 1] = -nums[n - 1]
        return res
"""
