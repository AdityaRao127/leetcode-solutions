class Solution(object):
    def romanToInt(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        values = {

            'I' : 1,
            'V' : 5,
            'X' : 10,
            'L' : 50,
            'C' : 100,
            'D' : 500,
            'M' : 1000,
        }

        roman_values = list(map(lambda c: values[c], s))
        total = sum(
            roman_values[i] if i == len(roman_values)-1 or roman_values[i] >= roman_values[i+1]
            else -roman_values[i]
            for i in range(len(roman_values))
        )
        return total

            
