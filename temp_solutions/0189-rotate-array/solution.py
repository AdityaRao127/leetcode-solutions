class Solution(object):
    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: None Do not return anything, modify nums in-place instead.
        """

        if(len(nums) <= 2 and k >1):
            if(k%2 == 0):
                return nums
            else:
                return nums.reverse()


        k = k % len(nums) # overflow
        nums.reverse()
        #7 6 5 4 3 2 1 

        nums[k:] = nums[k:][::-1]
        nums[:k] = nums[:k][::-1]
       
       # while(k >0):
        #    nums.insert(0, nums.pop())
         #   k-=1

        #nums.reverse()
                
