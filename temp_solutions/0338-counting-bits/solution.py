class Solution:
    def countBits(self, n: int) -> List[int]:
        
        arr = []
        i =0
        for i in range(n+1):
            binary_number = str(bin(i)[2:])
            count = sum(1 for num in binary_number if num == '1')
            arr.append(count)

        return arr
