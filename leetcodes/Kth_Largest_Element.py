import heapq
from typing import List
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = nums[:k]
        heapq.heapify(heap)
        for num in nums[k:]:
            if num > heap[0]:
                heapq.heapreplace(heap, num)

        return heap[0]
    
nums = [3,2,1,5,6,4]
k = 3
solver = Solution()
solver.findKthLargest(nums, k)