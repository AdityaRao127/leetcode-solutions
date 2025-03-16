# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        if not root:
            return False  # If root is empty, subRoot can't be a subtree

        # If the trees match exactly, return True
        if self.isSameTree(root, subRoot):
            return True

        # Recursively check left and right subtrees
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)

    def isSameTree(self, tree1: Optional[TreeNode], tree2: Optional[TreeNode]) -> bool:
        # If both trees are None, they match
        if not tree1 and not tree2:
            return True
        # If one is None but the other isn't, they don't match
        if not tree1 or not tree2:
            return False
        # Check values and recursively compare left & right subtrees
        return (tree1.val == tree2.val and 
                self.isSameTree(tree1.left, tree2.left) and 
                self.isSameTree(tree1.right, tree2.right))
