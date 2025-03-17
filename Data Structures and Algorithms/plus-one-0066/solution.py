class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        s = ""
        for digit in digits:
            s+=(str(digit))

        print(s)
        s = int(s) +  1 
        s = str(s)

        result = []
        for val in s:
            result.append(int(val))

        return result

