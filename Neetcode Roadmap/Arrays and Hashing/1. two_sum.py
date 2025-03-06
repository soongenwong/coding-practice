class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        prevMap = {}
        for i, n in enumerate(nums):
            diff = target - n
            if diff in prevMap:
                return [prevMap[diff], i]
            prevMap[n] = i
# the index of the 2 values that add up to give target value

#"prevMap", because this is a hash map that has all the previous values that went through the loop.
