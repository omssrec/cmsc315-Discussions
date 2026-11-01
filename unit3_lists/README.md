# Unit 3 Discussion: List Operations

## Overview

This assignment examines insertion, deletion, and searching in Python lists.

## Learning Objectives

- Insert values into a list
- Delete values from a list
- Search for values in a list
- Analyze list behavior and performance

## Requirements

1. Test insertion at the beginning, middle, and end.
2. Test deletion at the beginning, middle, and end.
3. Search for existing and missing values.
4. Demonstrate edge cases.
5. Create a real-world scenario.

## Scenario: Refueling Outage Core Load Sequence

I built the program around a nuclear plant refueling outage.  I tend to make projects in these assignments related to my field.  The fuel handling crew works from a **core load sequence**, which is an ordered list of fuel assembly IDs where index 0 is the next assembly the refueling bridge picks up.  During an outage the plans often change (although not so much with the fuel load, but bear with me), so every list operation mapped to a real event:

| Operation | Position | Event in the scenario |
|---|---|---|
| Insert | Beginning | A neutron-source assembly was moved to the front so it loads first |
| Insert | Middle | Engineering cleared a reconstituted assembly to load after F-207 |
| Insert | End | A late-arriving new assembly was added as the final load |
| Delete | Beginning | The next assembly was loaded into the core and came off the plan |
| Delete | Middle | An assembly that failed pre-load inspection was pulled |
| Delete | End | The last assembly was held back as a spare |
| Search | Found / missing | The spotter verified each ID against the plan before the crane moved; a missing ID meant "stop, do not load" |

Assembly IDs are invented for the demo.

## How I Implemented It

- **`insert_at(lst, index, value)`** used `list.insert()`. Comments explained that a Python list is a contiguous dynamic array, so every element at or after `index` had to shift right before the new value was written.  Front and middle inserts were O(n); appending at the end was O(1) amortized.
- **`delete_at(lst, index)`** validated the index before touching the list.  It accepted Python-style negative indexes (`-len(lst) <= index < len(lst)`), rejected non-integers and booleans, and returned `None` for anything invalid instead of letting `pop()` raise `IndexError`.  Valid deletes used `list.pop(index)`, which shifted the trailing elements left to close the gap.
- **`search_value(lst, value)`** was a hand-written linear search with `enumerate()`.  Because the list was ordered by load step rather than by ID, there was no sorted order to exploit, so it scanned sequentially and returned the first matching index or `-1`.

To make the cost of each operation visible, I added two helpers, `shifted_on_insert()` and `shifted_on_delete()`, and printed how many assemblies moved on every insert and delete.  The output showed 5 shifts for the front insert, 3 for the middle, and 0 for the end.  Search results also reported how many comparisons the scan needed.

I also added a `show()` helper that printed the list as numbered load steps, so the output read like the plan a crew would actually use.

## Edge Cases Tested

1. **Insert into an empty list** worked at index 0 with nothing to shift.
2. **Delete from an empty list** returned `None` without crashing.
3. **Delete at index 99** of a short list returned `None` and left the list unchanged.
4. **Delete with a string index** (`'2'`) was rejected by validation instead of raising `TypeError`.
5. **Search an empty list** returned `-1` immediately with zero comparisons.
6. **Out-of-range insert** (index 50 on a 3-item list) showed that `list.insert()` silently clamps to the end. This was convenient but could hide a bug.
7. **Duplicate IDs** showed that linear search only returns the first occurrence.

This seemed like a lot of edges cases, but none of them actually are specific to my project.  They all have to do with managing a list.  The point being that they seems like good edge cases to get used to testing.

## Extra: Front vs. End Insertion Benchmark

I timed 20,000 insertions three ways with `timeit`. On my run, `list.insert(0, x)` took roughly 100x longer than `list.append(x)`, while `deque.appendleft(x)` (a linked structure of memory blocks) stayed close to `append`.  Exact times vary by machine, but the gap illustrated the O(n) vs. O(1) difference.  Outage managers are always concerned about time.

## When a Linked List Outperforms an Array-Based List

A linked list wins when the workload is dominated by inserts and deletes at the front or at a position you already hold a reference to.  It relinks a couple of pointers instead of shifting every element after the change, and it never needs to reallocate and copy a whole block when it grows.  An array-based list still wins for random access by index (O(1) vs. O(n)), for appending at the end, and for cache-friendly sequential scans.

## Discussion Board Reflection

After completing the programming assignment, add this reflection to your initial discussion post in LEO.

Your reflection should be approximately 150–200 words and address the following questions:

1. What concepts or skills did you learn while completing this assignment?
2. What challenges did you encounter, and how did you overcome them?
3. How do list operations impact performance in real-world applications?

This assignment showed me that "insert" has costs further down the project from where i am inserting an item, and the true cost depends entirely on where it happens.  Printing the shift count after every insert and delete showed that.  Watching five fuel assemblies slide back for a front insert and none for an end insert explained O(n) versus O(1) better than any table could.  I also learned that `list.insert()` clamps out-of-range indexes instead of raising an error, which surprised me and is the kind of quiet behavior that can hide a bug.

My main challenge was deciding what counts as a valid index in `delete_at()`.  Python's own negative indexing and the fact that `True` is technically an int both had to be handled deliberately. I resolved it by writing out the valid range explicitly and testing the edges.

In real applications, list choice matters most at scale. Front-heavy workloads such as processing a work queue in arrival order punish an array, which is why the benchmark showed roughly a 100x gap.  Index-heavy workloads favor arrays, and front-heavy ones favor linked structures like `deque`.
