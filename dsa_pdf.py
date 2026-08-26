import sys
sys.path.append("C:/EIRA")
from tools.pdf_maker import notes_to_pdf
import subprocess

CONTENT = """
# DSA in Java — Basic to Interview Level

## 1. Arrays
- Declaration: int[] arr = new int[5]
- Access: arr[i] — O(1)
- Search: O(n) linear, O(log n) binary
- Sort: Arrays.sort(arr) — O(n log n)

## 2. Strings
- Immutable in Java
- StringBuilder for mutable
- charAt(), length(), substring()
- String.valueOf(), toCharArray()

## 3. Linked List
- Singly, Doubly, Circular
- Node class with data + next
- Insert: O(1) at head
- Search: O(n)

## 4. Stack
- LIFO — Last In First Out
- push(), pop(), peek(), isEmpty()
- Use: balanced brackets, undo operations
- Java: Stack class or Deque

## 5. Queue
- FIFO — First In First Out
- offer(), poll(), peek()
- Use: BFS, scheduling
- Java: LinkedList as Queue

## 6. HashMap
- Key-Value pairs
- put(), get(), containsKey()
- Time: O(1) average
- Use: frequency count, caching

## 7. Trees
- Binary Tree — max 2 children
- BST — left smaller, right greater
- Traversals: Inorder, Preorder, Postorder
- Height: O(log n) balanced

## 8. Sorting Algorithms
- Bubble Sort: O(n2) — easy
- Selection Sort: O(n2)
- Insertion Sort: O(n2) — best for small
- Merge Sort: O(n log n) — stable
- Quick Sort: O(n log n) — fastest avg

## 9. Searching
- Linear Search: O(n)
- Binary Search: O(log n) — sorted only
- BFS: O(V+E) — shortest path
- DFS: O(V+E) — cycle detection

## 10. Dynamic Programming
- Memoization — top down
- Tabulation — bottom up
- Famous problems: Fibonacci, Knapsack
- 0-1 Knapsack, LCS, LIS

## 11. Recursion
- Base case + recursive case
- Stack overflow if no base case
- Use: tree traversal, divide conquer

## 12. Graph
- Adjacency Matrix vs List
- BFS — shortest path unweighted
- DFS — cycle detection, topological sort
- Dijkstra — shortest path weighted

## Interview Must Know Topics
- Two Pointer technique
- Sliding Window
- Fast and Slow Pointer
- Merge Intervals
- Binary Search variations
- Tree BFS and DFS patterns
- DP on strings and arrays

## Time Complexity Cheatsheet
- Array access: O(1)
- Binary Search: O(log n)
- Linear Search: O(n)
- Sorting: O(n log n)
- HashMap ops: O(1)
- Tree operations: O(log n)

## Quick Summary
DSA interview mein Arrays, Strings, LinkedList,
Stack, Queue, Trees, Graphs, aur DP sabse important hain.
Har topic ka time complexity yaad rakhna zaroori hai.
"""

print("PDF ban rahi hai...")
path = notes_to_pdf("DSA in Java — Interview Guide", CONTENT)
print(f"PDF bani: {path}")
subprocess.Popen(["start", path], shell=True)