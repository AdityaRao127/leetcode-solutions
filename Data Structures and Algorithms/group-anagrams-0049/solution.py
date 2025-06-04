class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        ang_map = {}
        for original in strs:
            word = "".join(sorted(original))
            if word not in ang_map:
                ang_map[word] = [original]
            else:
                ang_map[word].append(original)

        
        return list(ang_map.values())

