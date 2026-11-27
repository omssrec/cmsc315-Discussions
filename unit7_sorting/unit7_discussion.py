"""
===========================================================
UNIT 7 DISCUSSION: SORTING ALGORITHMS (BUBBLE SORT VS MERGE SORT)
===========================================================

STUDENT INSTRUCTIONS:

This project explores two fundamental sorting algorithms:
- Bubble Sort (iterative, comparison-based)
- Merge Sort (recursive, divide-and-conquer)

Your goal is to demonstrate both your coding ability and your
understanding of algorithm efficiency and behavior.

-----------------------------------------------------------
SCENARIO: FINDING THE "FIRST-OUT" AFTER A REACTOR TRIP
When a reactor trips, dozens of alarms come in within a few
seconds.  The operators need to know which alarm came in FIRST,
because the first-out points to the cause and everything after
it is just the plant reacting.  A sequence-of-events recorder
timestamps each alarm in milliseconds, but the plant computer
hands them over in polling order, not time order.  Sorting by
timestamp puts the story back in order.  All alarm names and
times are invented.
-----------------------------------------------------------
"""

import random


def bubble_sort(lst, stats=None):
    """
    TODO (Student):
    Implement Bubble Sort.

    Requirements:
    - Create a copy of the original list.
    - Compare adjacent elements.
    - Swap elements when they are out of order.
    - Continue until the list is sorted.
    - Return the sorted list.
    - Add meaningful comments.

    stats (optional): a dict that counts comparisons and swaps
    for the performance analysis.
    """
    data = lst.copy()          # work on a copy so the caller's list is untouched
    n = len(data)

    # Each pass "bubbles" the largest remaining value to the end, so after
    # pass i the last i positions are final and don't need to be checked.
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if stats is not None:
                stats["comparisons"] += 1
            # Swap when the left value is bigger than its neighbor.
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True
                if stats is not None:
                    stats["swaps"] += 1
        # A full pass with no swaps means the list is already sorted,
        # so stop early instead of running the remaining passes.
        if not swapped:
            break
    return data


def merge_sort(lst, stats=None):
    """
    TODO (Student):
    Implement Merge Sort.

    Requirements:
    - Use recursion.
    - Divide the list into smaller halves.
    - Sort each half recursively.
    - Merge the sorted halves together.
    - Return the sorted list.
    - Add meaningful comments.

    """
    # Base case: a list of 0 or 1 items is already sorted.
    if len(lst) <= 1:
        return lst.copy()

    # Divide: split at the midpoint.  Slicing makes new lists, so the
    # original is never modified.
    mid = len(lst) // 2
    left = merge_sort(lst[:mid], stats)     # sort the left half
    right = merge_sort(lst[mid:], stats)    # sort the right half

    # Combine: two sorted halves become one sorted list.
    return merge(left, right, stats)


def merge(left, right, stats=None):
    """
    TODO (Student):
    Implement the merge step used by Merge Sort.

    Requirements:
    - Compare values from the left and right lists.
    - Build a new sorted result list.
    - Append any remaining values.
    - Return the merged sorted list.
    - Add meaningful comments.
    """
    result = []
    i = j = 0   # i walks the left list, j walks the right list

    # Compare the front of each list and take the smaller one.
    while i < len(left) and j < len(right):
        if stats is not None:
            stats["comparisons"] += 1
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # One list ran out.  Everything left in the other one is already
    # sorted and larger than what's in result, so add it as-is.
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def run_both(label, data):
    """Sort one dataset with both algorithms and show that they agree."""
    b = bubble_sort(data)
    m = merge_sort(data)
    print(f"  {label}")
    print(f"    Original:    {data}")
    print(f"    Bubble Sort: {b}")
    print(f"    Merge Sort:  {m}")
    print(f"    Results match: {b == m}")


def count_work(sort_func, data):
    """Return (comparisons, swaps) for one sort of data."""
    stats = {"comparisons": 0, "swaps": 0}
    sort_func(data, stats)
    return stats["comparisons"], stats["swaps"]


def main():
    print("=== UNIT 7: SORTING ALGORITHMS ===")

    # ===============================
    # TODO (Student): DATASET #1
    # ===============================
    #
    # Requirements:
    # 1. Create an unsorted list containing at least 7 values.
    # 2. Display the original list.
    # 3. Sort the list using Bubble Sort.
    # 4. Sort the same list using Merge Sort.
    # 5. Clearly label and display all results.

    print("\n=== DATASET #1 ===")
    # Alarm times in milliseconds, in the order the plant computer polled them.
    alarm_ms = [1851, 0, 2410, 390, 1702, 1840, 2950, 1853]
    run_both("Alarm timestamps (ms) in polling order:", alarm_ms)

    # ===============================
    # TODO (Student): DATASET #2
    # ===============================
    #
    # Requirements:
    # 1. Create a second dataset.
    # 2. Use different values than Dataset #1.
    # 3. Sort using both algorithms.
    # 4. Compare the results.

    print("\n=== DATASET #2 ===")
    # Different values AND a different type: annunciator window IDs (strings).
    # Both sorts only use < and >, so they work on anything comparable.
    windows = ["F-12", "A-03", "C-07", "A-01", "E-22", "B-15", "D-04"]
    run_both("Annunciator window IDs (strings, alphabetical):", windows)

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least two edge cases.
    #
    # Example ideas:
    # - Empty list
    # - Already sorted list
    # - Reverse-sorted list
    # - List with duplicate values
    # - Single-element list
    #
    # Explain what happens in each case.

    print("\n=== EDGE CASE TESTS ===")

    run_both("1. Empty list:", [])
    print("    -> Bubble's loops never run; merge hits its base case right away.")

    # For sorted and reversed lists, count the work to show best vs worst case.
    already = [1, 2, 3, 4, 5, 6, 7, 8]
    run_both("2. Already sorted:", already)
    bc, bs = count_work(bubble_sort, already)
    mc, _ = count_work(merge_sort, already)
    print(f"    -> Bubble: {bc} comparisons, {bs} swaps (one pass, then early exit).")
    print(f"       Merge:  {mc} comparisons (still splits and merges everything).")

    backward = already[::-1]
    run_both("3. Reverse sorted:", backward)
    bc, bs = count_work(bubble_sort, backward)
    mc, _ = count_work(merge_sort, backward)
    print(f"    -> Bubble: {bc} comparisons, {bs} swaps (worst case: every pair swaps).")
    print(f"       Merge:  {mc} comparisons (same as the sorted case).")

    # ===============================
    # PERFORMANCE ANALYSIS
    # ===============================
    # Count comparisons on random lists of growing size.  Counting
    # comparisons doesn't depend on how fast the computer is.
    print("\n=== PERFORMANCE ANALYSIS ===")
    random.seed(315)    # fixed seed so the counts are the same every run
    print(f"  {'n':>5} | {'Bubble comparisons':>18} | {'Merge comparisons':>17}")
    print("  " + "-" * 46)
    for n in (10, 100, 1000, 2000):
        data = [random.randint(0, 100_000) for _ in range(n)]
        bc, _ = count_work(bubble_sort, data)
        mc, _ = count_work(merge_sort, data)
        print(f"  {n:>5} | {bc:>18,} | {mc:>17,}")
    print("  Doubling n from 1000 to 2000 roughly quadruples bubble's work")
    print("  (O(n^2)) but only slightly more than doubles merge's (O(n log n)).")

    # ===============================
    # REAL-WORLD EXAMPLE: FIRST-OUT AFTER A REACTOR TRIP
    # ===============================
    print("\n=== REAL-WORLD EXAMPLE: FIRST-OUT AFTER A REACTOR TRIP ===")

    # (time in ms, alarm name) in the order the plant computer received them.
    # Tuples sort by the first item, so sorting puts them in time order.
    polled = [(1851, "RX TRIP BKR A OPEN"),
              (1853, "RX TRIP BKR B OPEN"),
              (0,    "MFW PUMP A TRIP"),
              (2410, "TURBINE TRIP"),
              (390,  "MFW HEADER PRESS LO"),
              (2950, "AFW PUMP A START"),
              (1702, "SG A LEVEL LO-LO"),
              (1840, "SG B LEVEL LO-LO"),
              (2415, "GENERATOR TRIP")]

    print("  Alarms as received (polling order):")
    for ms, name in polled:
        print(f"    t+{ms:>5} ms  {name}")

    timeline = merge_sort(polled)
    print("\n  Sorted timeline (merge_sort):")
    for ms, name in timeline:
        print(f"    t+{ms:>5} ms  {name}")
    print(f"\n  FIRST-OUT: {timeline[0][1]} at t+{timeline[0][0]} ms")


if __name__ == "__main__":
    main()
