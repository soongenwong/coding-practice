# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        
        def rec(root: ListNode, cur: ListNode) -> ListNode:
            
            if not cur:
                return root
            root = rec(root, cur.next)

            if not root:
                return None
            tmp = None

            if root == cur or root.next == cur:
                cur.next = None
            else:
                tmp = root.next
                root.next = cur
                cur.next = tmp
            return tmp
        
        head = rec(head, head.next)