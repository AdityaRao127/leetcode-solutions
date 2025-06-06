# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def reverseList(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """

        current = head
        prev = None

        while current != None:
            next = current.next
            current.next = prev
            prev = current
            current = next

        return prev
        """
        1️⃣ Save current.next → next_temp.
2️⃣ Reverse the link → current.next = prev.
3️⃣ Move prev forward → prev = current.
4️⃣ Move current forward → current = next_temp.
        """
