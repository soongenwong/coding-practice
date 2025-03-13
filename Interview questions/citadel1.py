def bestsumdownwardtreepath(parent, values):
    # Build the tree representation
    n = len(values)
    tree = [[] for _ in range(n)]
   
    for i in range(1, len(parent)):
        tree[parent[i]].append(i)
   
    # Memoization to avoid recalculating paths
    memo = {}
   
    def dfs(node):
        if node in memo:
            return memo[node]
       
        # Base case: if no children
        if not tree[node]:
            return values[node]
       
        # Find the best path from children
        max_child_sum = 0
        for child in tree[node]:
            max_child_sum = max(max_child_sum, dfs(child))
       
        # Return value of current node plus best path from children
        # If the best child path is negative, don't include it
        memo[node] = values[node] + max(0, max_child_sum)
        return memo[node]
   
    # Find the best path starting from any node
    best_sum = float('-inf')
    for i in range(n):
        best_sum = max(best_sum, dfs(i))
   
    return best_sum