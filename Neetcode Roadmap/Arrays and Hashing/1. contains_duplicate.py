from typing import List

class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False

def main():
    solution = Solution()
    
    nums1 = [1, 2, 3, 1]
    print(f"Input: nums = {nums1}")
    print(f"Output: {solution.hasDuplicate(nums1)}")
    
    nums2 = [1, 2, 3, 4]
    print(f"\nInput: nums = {nums2}")
    print(f"Output: {solution.hasDuplicate(nums2)}")
    
    nums3 = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]
    print(f"\nInput: nums = {nums3}")
    print(f"Output: {solution.hasDuplicate(nums3)}")

    print("\nEnter numbers separated by spaces:")
    user_input = input()
    user_nums = [int(x) for x in user_input.split()]
    print(f"Input: nums = {user_nums}")
    print(f"Output: {solution.hasDuplicate(user_nums)}")

if __name__ == "__main__":
    main()

#if there are 2 identical calues, return true