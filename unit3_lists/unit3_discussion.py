"""
==================================================
Unit 3 DISCUSSION: List Operations (Insert, Delete, Search)
==================================================

INSTRUCTIONS:
This assignment focuses on understanding how lists behave when elements
are inserted, removed, and searched. You will analyze how Python lists
shift elements in memory and how different operations impact performance.
"""
SCENARIO:
During a nuclear plant refueling outage, the fuel handling crew works from a
CORE LOAD SEQUENCE: an ordered list of fuel assembly IDs.  Position 0 is the
next assembly the refueling bridge will pick up; the last position is the
final assembly to be loaded.  The plan changes constantly during an outage
(not really, but for the purposes of this proejct we will go with it):
engineering adds assemblies, inspections pull assemblies, and the crew must
verify every ID against the plan before the crane moves.  That makes it a
great okace ti utiize the methods form this unit: insert, delete, and search, 
and for seeing why the position of an operation matters.

import timeit
from collections import deque

def insert_at(lst, index, value):
    """
    TODO (Student):
    Insert a value into the list at the specified index.

    Requirements:
    - Use a list operation to insert the value.
    - Add comments explaining what happens to existing elements
      after an insertion occurs.
    - Use comments to explain how insertion performance may vary depending on
      where the insertion occurs.
    """
    # A Python list is a dynamic ARRAY: its elements sit in one contiguous
    # block of memory.  To open a gap at `index`, every element from `index`
    # to the end must slide one slot to the right first, and only then is the
    # new value written into the gap.
    #
    # Performance depends on WHERE the insert lands:
    #   - index 0 (front)  -> all n elements shift              -> O(n)
    #   - middle           -> about n/2 elements shift          -> O(n)
    #   - end (index len)  -> nothing shifts                    -> O(1) amortized
    # "Amortized" because occasionally the array is full and Python must
    # allocate a bigger block and copy everything over, but that is rare
    # enough that the average cost per append stays constant.
    #
    lst.insert(index, value)


def delete_at(lst, index):
    """
    TODO (Student):
    Remove and return the value at the specified index.

    Requirements:
    - Validate that the index exists.
    - Return the removed value.
    - Return None if the index is invalid.
    - Add comments explaining why index validation and safe deletion are important.
    """
    # Validation comes BEFORE touching the list.  Without it, lst.pop() on a
    # bad index raises IndexError and can crash the whole program.  In the
    # refueling scenario, a crash halfway through updating the plan would
    # leave the sequence in an unknown state.  Returning None gives the caller a clear,
    # checkable "nothing was removed" signal instead.
    #
    # I accept Python-style negative indexes (-1 = last item), so the valid
    # range is -len(lst) <= index < len(lst).  Non-integers are rejected too. 
    if not isinstance(index, int) or isinstance(index, bool):
        return None
    if not -len(lst) <= index < len(lst):
        return None   # also covers the empty list, where no index is valid

    # pop(index) removes the element and then slides everything AFTER it one
    # slot LEFT to close the gap, the mirror image of insertion.
    return lst.pop(index)


def search_value(lst, value):
    """
    TODO (Student):
    Search for a value within the list.

    Requirements:
    - Return the index if the value is found.
    - Return -1 if the value is not found.
    - Add comments explaining why this is a linear search and why it scans sequentially.
    """
    # This is a LINEAR search, it starts at index 0 and compare each element in
    # order until a match is found or the list runs out.
    #
    # It has to scan sequentially because the list is ordered by LOAD STEP,
    # not by fuel assembly ID.  With no sorted order to exploit, there is no way
    # to jump ahead.
    #
    # The cost is for the best case O(1) (first element), worst case O(n) (last element or
    # missing entirely).
    for i, item in enumerate(lst):
        if item == value:
            return i
    return -1

# Helpers I added to make the output readable (not part of the starter).

def show(label, lst):
    """Print the sequence as numbered load steps (1-based for humans)."""
    print(f"  {label}")
    if not lst:
        print("    (empty -- nothing scheduled)")
        return
    for step, assembly in enumerate(lst, start=1):
        print(f"    Step {step:>2}: {assembly}")


def shifted_on_insert(lst, index):
    """How many existing elements move right when inserting at `index`."""
    index = max(0, min(index, len(lst)))   # mirror insert()'s clamping
    return len(lst) - index


def shifted_on_delete(lst, index):
    """How many elements move left after deleting at a valid `index`."""
    if index < 0:
        index += len(lst)
    return len(lst) - index - 1

def main():
    print("=== UNIT 3: LIST OPERATIONS ===")
    print("Scenario: refueling outage core load sequence")

    # ===============================
    # TODO (Student): INSERTION TESTS
    # ===============================
    #
    # Requirements:
    # 1. Create a list containing several values.
    # 2. Display the original list.
    # 3. Test insertion at:
    #    - the beginning
    #    - the middle
    #    - the end
    # 4. Display the list after each insertion.
    # 5. Use comments to explain each step in the implementation.

    print("\n=== INSERTION TESTS ===")
    print("TODO: Create a list and demonstrate insertions.")

    # Step 1: build the load plan (five assemblies in load order).
    sequence = ["F-114", "F-207", "F-031", "F-188", "F-062"]
    show("Original approved sequence:", sequence)

    # Step 2: BEGINNING.  A neutron-source assembly must be loaded first so
    # the source-range neutron detectors have something to see.  Every existing
    # assembly slides back one step.
    moved = shifted_on_insert(sequence, 0)
    insert_at(sequence, 0, "SRC-01")
    print(f"\n  Inserted SRC-01 at the FRONT -> {moved} assemblies shifted")
    show("After front insert:", sequence)

    # Step 3: MIDDLE.  Reactor Engineering clears a reconstituted assembly to go in
    # right after F-207.  Only the assemblies behind that point shift.
    middle = search_value(sequence, "F-207") + 1
    moved = shifted_on_insert(sequence, middle)
    insert_at(sequence, middle, "R-009")
    print(f"\n  Inserted R-009 after F-207 (index {middle}) "
          f"-> {moved} assemblies shifted")
    show("After middle insert:", sequence)

    # Step 4: END.  A new assembly clears receipt inspection late and is
    # added as the final load.  Nothing in front of it moves.
    moved = shifted_on_insert(sequence, len(sequence))
    insert_at(sequence, len(sequence), "N-301")
    print(f"\n  Inserted N-301 at the END -> {moved} assemblies shifted")
    show("After end insert:", sequence)

    # Extra test beyond the starter: a negative index inserts BEFORE the
    # element at that position.  -1 means "just before the last item".
    insert_at(sequence, -1, "F-150")
    print("\n  Extra: insert_at(seq, -1, 'F-150') places it BEFORE the last item")
    show("After negative-index insert:", sequence)

    # ===============================
    # TODO (Student): DELETION TESTS
    # ===============================
    #
    # Requirements:
    # 1. Delete an item from:
    #    - the beginning
    #    - the middle
    #    - the end
    # 2. Display the removed value.
    # 3. Display the updated list after each deletion.
    # 4. Use comments to clearly explain what is happening in the output.

    print("\n=== DELETION TESTS ===")
    print("TODO: Demonstrate deletions from multiple positions.")

    # BEGINNING: the refueling bridge loads the next assembly, so it comes off the
    # front of the plan.  Every remaining assembly moves up one step --
    # this is the most expensive delete position.
    moved = shifted_on_delete(sequence, 0)
    removed = delete_at(sequence, 0)
    print(f"  Loaded into core (removed from front): {removed} "
          f"-> {moved} assemblies shifted up")
    show("Remaining sequence:", sequence)

    # MIDDLE: F-031 fails its pre-load visual inspection and is pulled from
    # the plan.  Only the assemblies after it close the gap.
    middle = search_value(sequence, "F-031")
    moved = shifted_on_delete(sequence, middle)
    removed = delete_at(sequence, middle)
    print(f"\n  Pulled for failed inspection (index {middle}): {removed} "
          f"-> {moved} assemblies shifted up")
    show("Remaining sequence:", sequence)

    # END: the final assembly is held back as a spare.  Removing the last
    # element shifts nothing, so this is O(1).
    removed = delete_at(sequence, -1)
    print(f"\n  Held back as spare (removed from end): {removed} "
          f"-> 0 assemblies shifted")
    show("Remaining sequence:", sequence)

    # ===============================
    # TODO (Student): SEARCH TESTS
    # ===============================
    #
    # Requirements:
    # 1. Search for a value that exists.
    # 2. Search for a value that does not exist.
    # 3. Display the search results with clear explanations.
    # 4. Use comments to explain each step.

    print("\n=== SEARCH TESTS ===")
    print("TODO: Demonstrate searching for values.")

    # Before the crane grapples an assembly, the spotter reads the ID off the
    # assembly and confirms it is in the plan -- a real-world linear search.
    for target in ["F-188", "R-009", "F-999"]:
        idx = search_value(sequence, target)
        if idx != -1:
            # Found: report both the 0-based index and the human load step,
            # and how many comparisons the linear scan needed (idx + 1).
            print(f"  {target}: FOUND at index {idx} (load step {idx + 1}), "
                  f"{idx + 1} comparison(s)")
        else:
            # Not found: -1 is the sentinel.  A miss always costs a full scan.
            print(f"  {target}: NOT IN PLAN (returned -1) after checking all "
                  f"{len(sequence)} entries -> STOP, do not load")



    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least two edge cases.
    #
    # Example ideas:
    # - Delete using an invalid index
    # - Search for a missing value
    # - Insert into an empty list
    # - Delete from an empty list
    # - Use comments to explain each edge case.

    print("\n=== EDGE CASES ===")
    print("TODO: Demonstrate at least two edge cases.")

    # Edge 1: insert into an EMPTY list.  At the start of a reload there is
    # no plan yet; index 0 is the only valid position and nothing shifts.
    new_plan = []
    insert_at(new_plan, 0, "SRC-02")
    print(f"  1) Insert into empty list -> {new_plan}")

    # Edge 2: delete from an EMPTY list.  Every assembly has been loaded;
    # asking for "the next one" must fail safely, not crash.
    empty = []
    print(f"  2) Delete from empty list -> {delete_at(empty, 0)} "
          "(no crash, None returned)")

    # Edge 3: delete with an index past the end (step 99 of a short plan).
    print(f"  3) Delete index 99 from {len(sequence)}-item list -> "
          f"{delete_at(sequence, 99)}; list unchanged: {sequence}")

    # Edge 4: delete with a non-integer index, e.g. a step number typed as
    # text.  Validation rejects it rather than raising TypeError.
    print(f"  4) Delete with index '2' (a string) -> {delete_at(sequence, '2')}")

    # Edge 5: search an EMPTY list.  The loop body never runs, so -1 comes
    # back immediately -- correct, and zero comparisons.
    print(f"  5) Search empty list for 'F-188' -> {search_value([], 'F-188')}")

    # Edge 6: out-of-range INSERT.  Python does not raise an error here; it
    # clamps the index to the end.  That is convenient but can hide a bug --
    # someone who meant "step 50" silently gets "last step".
    demo = ["A", "B", "C"]
    insert_at(demo, 50, "Z")
    print(f"  6) insert_at(['A','B','C'], 50, 'Z') -> {demo} "
          "(clamped to end, no error)")

    # Edge 7: duplicate values.  Linear search returns the FIRST match, so a
    # duplicated ID in a plan would hide the second entry.
    dupes = ["F-114", "F-207", "F-114"]
    print(f"  7) Search {dupes} for 'F-114' -> {search_value(dupes, 'F-114')} "
          "(first occurrence only)")


    # My addition: Why Position Matters
    # Time 20,000 front insertions into a Python list (array: every insert
    # shifts everything) versus a deque (linked blocks: no shifting), and
    # compare with appending to the end of a list.

    # Outage managers are always interested in how much time is left to complete the fuel load.
    # Even the time the program takes to run will be of concern to them.
    
    print("\n=== EXTRA: FRONT vs END INSERTION COST ===")
    n = 20_000

    def list_front():
        lst = []
        for i in range(n):
            lst.insert(0, i)

    def list_end():
        lst = []
        for i in range(n):
            lst.append(i)

    def deque_front():
        dq = deque()
        for i in range(n):
            dq.appendleft(i)

    results = {
        "list.insert(0, x)    (array, front) ": timeit.timeit(list_front, number=1),
        "list.append(x)       (array, end)   ": timeit.timeit(list_end, number=1),
        "deque.appendleft(x)  (linked, front)": timeit.timeit(deque_front, number=1),
    }
    fastest = min(results.values())
    for name, secs in results.items():
        print(f"  {name}: {secs * 1000:8.2f} ms  ({secs / fastest:5.1f}x)")
    print("  Takeaway: the array pays for front inserts by shifting; the linked")
    print("  structure and the array's tail end do not.")


if __name__ == "__main__":
    main()
