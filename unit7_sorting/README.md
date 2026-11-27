# Unit 7 Discussion: Sorting Algorithms

## Overview

This assignment compares Bubble Sort and Merge Sort.

## Learning Objectives

- Implement Bubble Sort
- Implement Merge Sort
- Understand divide-and-conquer
- Compare algorithm efficiency

## Requirements

1. Test Bubble Sort and Merge Sort.
2. Use multiple datasets.
3. Demonstrate edge cases.
4. Analyze performance.
5. Create a real-world sorting example.

## Scenario: Finding the "First-Out" After a Reactor Trip

When a reactor trips, the control room goes from quiet to dozens of alarms in about three seconds.  The question that matters is which alarm came in **first**.  This is called the 'first-out' and is the indication of what caused the automatic trip.  The first-out points to the cause, and almost everything after it is just the plant responding the way it was designed to.  A sequence-of-events recorder timestamps every alarm to the millisecond, but in my scenario the plant computer hands them over in polling order, not time order.  Sorting by timestamp turns the pile back into a timeline.  All alarm names and times are invented.

## How I Implemented It

- **Bubble Sort:** works on a copy, compares neighbors, and swaps when the left value is bigger.  Each pass pushes the largest remaining value to the end, so the inner loop gets one step shorter every pass.  A `swapped` flag stops the sort as soon as a full pass makes no swaps.
- **Merge Sort:** recursive.  The base case is a list of 0 or 1 items.  Otherwise it splits at the midpoint, sorts each half, and calls `merge()` to combine them.
- **merge():** walks two sorted lists with two indexes, takes the smaller front value each time, then adds whatever is left over from the list that didn't run out.
- **Dataset #1:** 8 alarm timestamps in polling order.
- **Dataset #2:** annunciator window IDs (strings). Both sorts only use `<` and `>`, so they work on text as well as numbers.
- **Counting comparisons:** both sorts take an optional `stats` dictionary that counts comparisons and swaps, which gave me real numbers for the performance analysis.

## Edge Cases Tested

1. **Empty list:** bubble's loops never run, and merge sort hits its base case right away. Both return `[]`.
2. **Already sorted (8 items):** bubble made 7 comparisons and 0 swaps, then quit early.  Merge sort made 12 because it splits and merges no matter what.  This is the one case where bubble wins.
3. **Reverse sorted (8 items):** bubble's worst case, 28 comparisons and 28 swaps (every pair).  Merge sort made the same 12 as the sorted case.

## Performance Analysis

Comparison counts on random lists (seeded, so the counts are the same every run):

| n | Bubble comparisons | Merge comparisons |
|------:|------------:|-----------:|
| 10 | 44 | 25 |
| 100 | 4,914 | 548 |
| 1,000 | 498,680 | 8,699 |
| 2,000 | 1,996,722 | 19,399 |

Going from 1,000 to 2,000 items multiplied bubble's work by 4.0 and merge's by about 2.2.  That is O(n²) vs O(n log n) showing up in real numbers.

## Real-World Example

Nine alarms arrive jumbled: the reactor trip breakers show up first and the cause shows up third.  After `merge_sort()`, the timeline reads like a post-trip review:

```
t+    0 ms  MFW PUMP A TRIP          <- first-out
t+  390 ms  MFW HEADER PRESS LO
t+ 1702 ms  SG A LEVEL LO-LO
t+ 1840 ms  SG B LEVEL LO-LO
t+ 1851 ms  RX TRIP BKR A OPEN
t+ 1853 ms  RX TRIP BKR B OPEN
t+ 2410 ms  TURBINE TRIP
t+ 2415 ms  GENERATOR TRIP
t+ 2950 ms  AFW PUMP A START
```

Read in polling order, it looks like the trip breakers opened for no reason.  Sorted, it's clear the feedwater pump tripped first, steam generator levels dropped, and the reactor tripped on low-low level.  Sorting is what turns an alarm flood into a cause.

## Discussion Board Reflection

This assignment showed me that divide-and-conquer is less about splitting and more about merging.  Splitting a list in half is trivial.  The real work happens in `merge()`, and once two halves are sorted, combining them takes one pass.  The recursion just keeps cutting the problem down until every piece is already sorted.

My challenge was seeing why merge sort made the same 12 comparisons on a sorted list and a reversed one.  I traced both by hand and saw that merge sort splits the list the same way no matter what order the values are in, so the work barely changes.  Bubble sort's work depends entirely on how out of order the list is.

Bubble Sort is O(n²) on average and in the worst case, but with an early-exit flag it is O(n) on a list that is already sorted.  It sorts in place, uses almost no extra memory, and is easy to verify, so it is reasonable for tiny or nearly sorted lists.  Merge Sort is O(n log n) in every case and stable, but it needs O(n) extra memory for the merged lists.  For anything beyond a few dozen items, Merge Sort is the better choice.
