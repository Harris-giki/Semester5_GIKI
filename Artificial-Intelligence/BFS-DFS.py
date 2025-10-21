from binarytree import tree
from collections import deque
import time
import matplotlib.pyplot as plt

def bfs(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])

    while queue:
        node =queue.popleft()
        result.append(node.value)

        if node.left:
            queue.append(node.left)

        if node.right:
            queue.append(node.right)
    return result


def dfs(root):
    if not root:
        return []
    
    result = []

    #pre order traversal of dfs(root->left->right)
    def traverse(node):
        if not node:
            return    
        result.append(root.value)
        traverse(node.left)
        traverse(node.right)
    traverse(root) #starts the dfs traversal
    return result

tree_sizes = [3, 4, 5, 6]
bfs_times = []
dfs_times = []

for size in tree_sizes:
    root= tree(height=None, isperfect=False)
    while root.size<size:
        root= tree(height=None, isperfect=False)

start = time.time()
bfs(root)
end=time.time()
bfs_times.append(end-start)

start = time.time()
dfs(root)
end = time.time()
dfs_times.append(end-start)

plt.plot(tree_sizes, bfs_times, label='BFS Time', marker='o')
plt.plot(tree_sizes, dfs_times, label='DFS Time', marker='s')
plt.xlabel('Number of Nodes in Tree')
plt.ylabel('Time (seconds)')
plt.title('BFS vs DFS Time Complexity')
plt.legend()
plt.grid(True)
plt.show()