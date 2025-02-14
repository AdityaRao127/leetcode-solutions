class Solution(object):
    def plusOne(self, digits):
        changed = False
        pos = -1
        for i in range(len(digits)):
            if digits[i] != 9:
                pos = i
        if pos == -1:
            for i in range(len(digits)):
                digits[i] = 0
            digits.insert(0, 1)
        else:
            digits[pos] += 1
            for i in range(pos + 1, len(digits)):
                digits[i] = 0
        return digits

