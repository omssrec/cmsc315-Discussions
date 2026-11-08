# Unit 4 Discussion: Binary Search Trees

## Overview

This assignment introduces Binary Search Trees (BSTs) and recursive tree operations.

## Learning Objectives

- Build a BST
- Insert values recursively
- Search recursively
- Perform in-order traversal
- Understand BST organization

## Requirements

1. Build a BST.
2. Insert multiple values.
3. Demonstrate in-order traversal.
4. Test searching.
5. Demonstrate edge cases.
6. Create a real-world BST example.

## Scenario: Borehole Instrument Depth Registry

As usual, I tied this project to my field.  Picture a small reactor installed at the bottom of a borehole about a mile deep, with instruments strung down the hole.  This is the invention of my current employer and a project I am working on.  I built a BST keyed by each instrument's **depth in feet**, so the two directions of the tree line up with the hole itself:

| Tree direction | Meaning in the borehole |
|---|---|
| Left child | Shallower |
| Right child | Deeper |
| In-order traversal | Reading the hole from the top down |

Each comparison during a search is a decision to look shallower or deeper, and it rules out the whole other section of the hole.  The depths and instrument tags are hypothetical and used for the demo.

## How I Implemented It

- **`Node`** stores the depth as `value`, plus `left` and `right` references to the shallower and deeper subtrees.
- **`insert()` / `_insert_recursive()`**: the helper goes left for smaller values and right for larger ones.  When it reaches an empty spot (`None`), it creates the new node and returns it so the parent can attach it.  Every call returns its node reference, which is also how an empty tree gets its first root.  A duplicate depth hits the `==` case and is ignored, since two instruments can't share a depth.
- **`search()` / `_search_recursive()`** have two base cases: an empty subtree means not found, and an equal value means found.  Otherwise, the search only goes into the one subtree that could contain the value.
- **`inorder()` / `_inorder_recursive()`** visit left, node, right.  Since everything smaller is on the left and everything larger is on the right at every level, the output comes out sorted.

In `main()` I inserted 9 instruments in a random order (4,100 ft first, so it became the root), with values landing on both sides.  The in-order traversal turned that jumbled insert order into the borehole read from the top down.  I searched for two depths that have instruments (3,300 and 5,200 ft) and two that don't (2,000 and 6,000 ft), with comments tracing the shallower/deeper path each search takes.  I used a small dictionary of instrument tags only to make the output readable; the tree itself stores just the depths.

## Edge Cases Tested

1. **Traverse an empty tree** returned `[]` because the helper hits its `None` base case right away.
2. **Search an empty tree** returned `False` for the same reason.
3. **One-node tree** traversed to `[50]`.  Searching 50 returned `True`, and searching 600 returned `False`.
4. **Duplicate value**: inserting 3,300 ft a second time was ignored.  The tree still had 9 depths, and 3,300 appeared only once.

## Real-World Interpretation

A BST works well when order matters, not just whether something exists.  In this scenario, an in-order traversal gives the instruments from the top of the hole to the bottom with no sorting step.  Compared with a sorted Python list, a BST avoids shifting elements on every insert (the Unit 3 lesson).  Compared with a dictionary, it keeps the keys in order.

## Discussion Board Reflection

After completing the programming assignment, add this reflection to your initial discussion post in LEO.

Your reflection should be approximately 150–200 words and address the following questions:

1. What concepts or skills did you learn while completing this assignment?
2. What challenges did you encounter, and how did you overcome them?
3. Explain BST behavior and compare to how ordering works to create efficiency as compared to other data structures.

This assignment made recursion feel concrete.  Each call to `_insert_recursive()` makes one decision, shallower or deeper, and hands the problem to a smaller subtree until it reaches an empty spot.  Seeing that the base case is exactly where the new node gets created helped the whole method click for me.

My main challenge was understanding why the helper has to return a node reference.  At first, returning the same node seemed pointless to me.  Tracing an insert into an empty tree by hand showed me that the return value is how the new node gets attached to its parent, and how the root gets set the first time.

A BST is efficient because of its ordering.  Each comparison eliminates an entire subtree, so a balanced tree searches in O(log n) instead of the O(n) a linear search needs.  A sorted list can also be searched quickly, but inserting into it means shifting elements.  A dictionary finds exact keys faster, but it doesn't keep them in order.  The BST gives up a little speed on exact lookups in exchange for keeping everything sorted.
