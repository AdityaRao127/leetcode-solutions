class Solution:
    def stringMatching(self, words: List[str]) -> List[str]:
        words.sort(key = len)
        matches = set()

        for i, small_word in enumerate(words): 
            for j in range(i+1, len(words)):
                if(small_word in words[j]):
                    matches.add(small_word)
                    break 

        return list(matches)
