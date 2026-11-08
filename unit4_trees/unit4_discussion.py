"""
=========================================================
UNIT 4 DISCUSSION: BINARY SEARCH TREES (BST)
=========================================================

INSTRUCTIONS:
This assignment focuses on understanding and implementing a
Binary Search Tree (BST).

You will complete and modify the provided code while explaining
key concepts in your own words using comments and output.

SCENARIO: BOREHOLE INSTRUMENT DEPTH REGISTRY
A small reactor sits at the bottom of a borehole about a mile deep, with
instruments strung down the hole.  The BST is keyed by each instrument's
DEPTH in feet, so the two directions of the tree match the hole:
    left child  -> SHALLOWER
    right child -> DEEPER
All depths and instrument tags are invented for this demo.
"""

class Node:
    def __init__(self, value):
        # value is the instrument's depth in feet.
        # left points to the subtree of shallower instruments,
        # right points to the subtree of deeper instruments.
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        # An empty tree is just a root reference that points at nothing.
        self.root = None

    def insert(self, value):
        """
        Insert a value into the BST.

        Every value in a node's LEFT subtree is smaller and every value in
        its RIGHT subtree is larger.  Insertion is where that rule gets
        enforced: at each node we compare and go to exactly one side.  If a
        value were ever placed on the wrong side, later searches would turn
        the wrong way at that node and never find it.
        """
        # The helper returns the (possibly new) root, so we reassign it.
        # This is how an empty tree gets its first node.
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        """
        Recursive BST insertion.  Returns the updated node reference.
        """
        # Base case: we reached an empty spot, so the new node goes here.
        if node is None:
            return Node(value)

        if value < node.value:
            # Shallower: keep going down the left subtree.
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            # Deeper: keep going down the right subtree.
            node.right = self._insert_recursive(node.right, value)
        # If value == node.value it is a duplicate.  Two instruments can't be
        # at the same depth, so it is ignored and the tree is unchanged.

        # Return this node so the parent's link to it stays intact.
        return node

    def search(self, value):
        """
        Return True if value is in the tree, False otherwise.

        A linear search checks items one at a time and can't rule anything
        out, so it is O(n).  In a BST each comparison tells us which side the
        value has to be on, so the whole other subtree is skipped.  In a
        balanced tree that cuts the remaining nodes roughly in half each
        step, which makes search O(log n).
        """
        return self._search_recursive(self.root, va

    def _search_recursive(self, node, value):
        """
        Recursive BST search.
        """
        # Ran off the bottom of the tree: the value isn't here.
        if node is None:
            return False
        # Exact match.
        if value == node.value:
            return True
        # Otherwise search only the one subtree that could contain it.
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)

    def inorder(self):
        """
        Return a list containing the values from an in-order traversal.
        """
        values = []
        self._inorder_recursive(self.root, values)
        return values

    def _inorder_recursive(self, node, values):
        """
        In-order traversal: left subtree, current node, right subtree.

        Everything smaller than a node is in its left subtree and everything
        larger is in its right subtree.  Visiting left, then the node, then
        right outputs all the smaller values, then the node, then all the
        larger values.  That is true at every level, so the full result
        comes out in ascending order.
        """
        if node is None:
            return
        self._inorder_recursive(node.left, values)    # shallower instruments
        values.append(node.value)                     # this instrument
        self._inorder_recursive(node.right, values)   # deeper instruments


def main():
    print("=== UNIT 4: BINARY SEARCH TREES ===")
    print("Scenario: borehole instrument depth registry (left = shallower, right = deeper)")

    # Instrument tags by depth, used only to make the output readable.
    # The tree itself stores just the depths.
    tags = {
        4100: "TE-410 lower casing thermocouple",
        1500: "SG-150 casing strain gauge",
        5150: "NI-515 neutron detector",
        50:   "PT-005 wellhead pressure transmitter",
        2400: "TE-240 mid-string thermocouple",
        4700: "CE-470 groundwater conductivity probe",
        5200: "TE-520 vessel RTD",
        600:  "TE-060 upper casing thermocouple",
        3300: "FE-330 coolant flow element",
    }

    # ===============================
    # TODO (Student): BUILD A TREE
    # ===============================
    #
    # Requirements:
    # 1. Create a BST object.
    # 2. Insert at least 7 values.
    # 3. Include values that go into both left
    #    and right subtrees.
    # 4. Display the values inserted.
    # 5. Use comments to explain why a BST is efficient at reducing search space for each step.

    print("\n=== TREE CONSTRUCTION ===")

    # Step 1: create an empty BST.
    registry = BST()

    # Step 2: insert 9 instruments in a random order.
    # 4,100 ft goes in first and becomes the root.  After that, every insert
    # starts at the root and makes one shallower/deeper decision per level,
    # so it only looks at a single path instead of every instrument:
    #   1,500 and 50 are shallower than 4,100 -> left subtree
    #   5,150 and 5,200 are deeper than 4,100 -> right subtree
    #   2,400 is shallower than 4,100 but deeper than 1,500 -> left, then right
    depths = [4100, 1500, 5150, 50, 2400, 4700, 5200, 600, 3300]
    for depth in depths:
        registry.insert(depth)
        print(f"  Inserted {depth:>5,} ft  {tags[depth]}")

    # Step 3: show that values landed on both sides of the root.
    print(f"\n  Root: {registry.root.value:,} ft")
    print(f"  Left of root (shallower): {registry.root.left.value:,} ft")
    print(f"  Right of root (deeper):   {registry.root.right.value:,} ft")

    # ===============================
    # TODO (Student): IN-ORDER TRAVERSAL
    # ===============================
    #
    # Requirements:
    # 1. Perform an in-order traversal.
    # 2. Display the traversal results.
    # 3. Use comments to explain why the traversal produces
    #    sorted output in a BST.

    print("\n=== IN-ORDER TRAVERSAL ===")

    # The depths were inserted out of order, but in-order traversal returns
    # them sorted because it visits shallower (left), then the node, then
    # deeper (right) at every level.  In this scenario, that means reading
    # the borehole from the top down.
    order = registry.inorder()
    print(f"  Inserted order: {depths}")
    print(f"  In-order:       {order}")
    print("  Borehole from top to bottom:")
    for depth in order:
        print(f"    {depth:>5,} ft  {tags[depth]}")

    # ===============================
    # TODO (Student): SEARCH TESTS
    # ===============================
    #
    # Requirements:
    # 1. Search for at least two values that exist.
    # 2. Search for at least two values that do not exist.
    # 3. Use comments to clearly explain the results.

    print("\n=== SEARCH TESTS ===")

    # Two depths that have instruments.
    # 3,300: 4,100 -> shallower, 1,500 -> deeper, 2,400 -> deeper, match.
    # 5,200: 4,100 -> deeper, 5,150 -> deeper, match.
    for depth in [3300, 5200]:
        print(f"  Search {depth:>5,} ft -> {registry.search(depth)}  ({tags[depth]})")

    # Two depths with no instrument.  The search follows one path until it
    # runs off the bottom of the tree, then returns False.
    # 2,000: 4,100 -> shallower, 1,500 -> deeper, 2,400 -> shallower, empty.
    # 6,000: deeper than everything, so it falls off the right side.
    for depth in [2000, 6000]:
        print(f"  Search {depth:>5,} ft -> {registry.search(depth)}  (no instrument at this depth)")

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least one edge case.
    #
    # Example ideas:
    # - Traverse an empty tree
    # - Search an empty tree
    # - Insert duplicate values
    # - Create a tree with only one node
    #
    # Use comments to explain what happens and why.

    print("\n=== EDGE CASES ===")

    # Edge 1: traverse an empty tree.  The root is None, so the helper hits
    # its base case right away and returns an empty list.
    empty = BST()
    print(f"  1) In-order of empty tree -> {empty.inorder()}")

    # Edge 2: search an empty tree.  Same base case, so it returns False.
    print(f"  2) Search empty tree for 3,300 -> {empty.search(3300)}")

    # Edge 3: a tree with only one node.  The root is also the only leaf.
    single = BST()
    single.insert(50)
    print(f"  3) One-node tree: in-order {single.inorder()}, "
          f"search 50 -> {single.search(50)}, search 600 -> {single.search(600)}")

    # Edge 4: duplicate value.  Inserting 3,300 again hits the == case and
    # is ignored, so the traversal still has 9 depths and only one 3,300.
    registry.insert(3300)
    after = registry.inorder()
    print(f"  4) Insert duplicate 3,300 -> {len(after)} depths, "
          f"3,300 appears {after.count(3300)} time(s)")




if __name__ == "__main__":
    main()
