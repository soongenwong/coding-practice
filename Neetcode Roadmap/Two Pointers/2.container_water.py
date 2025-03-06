class Solution:
    def maxArea(self, heights: List[int]) -> int:
        l, r = 0, len(heights) - 1
        result = 0

        while l < r:
            area = min(heights[l], heights[r]) * (r - l)
            result = max(result, area)
            if heights[l] < heights[r]:
                l += 1
            else:
                r -= 1
        return result

# usual 2 pointer question. compare the height on left and right, and move towards centre for higher values. 