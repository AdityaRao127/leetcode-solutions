class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = s.lower()
        s = s.strip()
        s = s.translate(str.maketrans('', '', string.punctuation))
        s = s.split()
        s = "".join(s)
        print(s)
        if(s[::-1] == s):
            return True

        return False

