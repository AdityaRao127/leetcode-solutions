class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        seen = set()

        for num in nums:
            if num not in seen:
                seen.add(num)
        
        print(seen)
        seen = sorted(seen)

        k = 0
        for x in seen:
            nums[k] = x
            k+=1

        return len(seen)
