class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        max_sum = 0
        num_dict = {}
        for num in nums:
            digit_sum = self.digit_sum(num)
            if digit_sum in num_dict:
                max_sum = max(max_sum, num + num_dict[digit_sum])
                num_dict[digit_sum] = max(num_dict[digit_sum], num)
            else:
                num_dict[digit_sum] = num
        return max_sum if max_sum != 0 else -1

    def digit_sum(self, val):
        return sum(int(digit) for digit in str(abs(val)))
