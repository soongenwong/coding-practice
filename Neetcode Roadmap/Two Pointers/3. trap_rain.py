class Solution:
    def trap(self, height: List[int]) -> int:
        if not height: #if input is empty
            return 0
        
        l, r = 0, len(height) - 1
        leftMax, rightMax = height[l], height[r]
        result = 0
        while l < r:
            if leftMax < rightmax:
                l += 1
                leftMax = max(leftMax, height[l])
                result += leftMax - height[l] #this adds the trapped water
            else:
                r -= 1
                rightMax = max(rightMax, height[r])
                result += rightMax - height[r]
        return result

#the "result" line adds the trapped water
#by comparing l < r, it ensures that the trapped water will always be bounded in the end, as it loops back. 