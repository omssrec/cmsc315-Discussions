# Unit 5 Discussion: Search Algorithms

## Overview

This assignment compares linear search and binary search.

## Learning Objectives

- Implement linear search
- Implement binary search
- Compare performance
- Analyze algorithm efficiency

## Requirements

1. Test both algorithms on a small dataset.
2. Test both algorithms on a large dataset.
3. Demonstrate edge cases.
4. Analyze performance.
5. Create a real-world search scenario.


## Scenario: Control Room Alarm Lookup

Once again I tied the project to my field.  When an alarm comes in on a control room panel, the operator really has two different search problems, and I realized they line up with the two algorithms:

| Question the operator asks | Data being searched | How it is ordered | Algorithm that works |
|---|---|---|---|
| "What does alarm 4410 mean?" | Alarm Response Procedure (ARP) index | By alarm point number | **Binary search** |
| "What alarmed in the half second after the trip?" | Sequence of Events (SOE) log | By time | **Binary search** (on time) |
| "When did point 3300 *first* alarm?" | The same SOE log | By time, **not** by point number | **Linear search only** |

The interesting part is the last two rows.  The SOE log is sorted for one question and unsorted for the other.  Whether a list counts as "sorted" depends on the key you are searching on.  All alarm numbers, titles, and events are invented for the demo.

## How I Implemented It

- **`linear_search(lst, target)`** walked the list from index 0 with `enumerate()` and returned the first matching index, or `-1`.  Comments explained that it can't rule anything out from one comparison, so the worst case checks all n elements, which makes it O(n).
- **`binary_search(lst, target)`** kept `low` and `high` bracketing the part of the list where the target could still be.  Each pass probed the middle and threw out the half that couldn't contain the target, so the bracket went n → n/2 → n/4 → … → 1.  That takes about log2(n) passes, which makes it O(log n).
- Both functions took an optional `stats` dictionary so the program could print **how many comparisons** each search used.  I wanted the output to show the work, not just the answer, because timing alone changes from run to run.  The comparison counts stay the same every time.
- **`first_at_or_after(sorted_lst, target)`** was my addition.  It's a binary search variation that returned the first index whose value was `>=` the target.  I needed it for the time-window question, because we are tlaking about actual mechanical systems here and the event usually occurs at laast 1 second, if not more, before the alarm actuation.
- A **`compare()`** helper ran both searches on the same list and printed the results side by side.

### Small dataset

The ARP index held 12 sorted alarm numbers.  Looking up alarm 4410 took linear search 9 comparisons and binary search 2 probes.  Binary search's first probe hit 3110, which eliminated 6 alarms with one comparison.  A mistyped alarm number (4400) took linear search all 12 comparisons to reject, and binary search rejected it in 4 probes.  At this size the difference was only a handful of comparisons.

### Large dataset

The plant computer point database held 1,000,000 sorted points (even numbers only, so every odd number was guaranteed missing).

| Search | Linear comparisons | Binary probes |
|---|---|---|
| Point near the end | 999,996 | 20 |
| Missing point | 1,000,000 | 20 |
| Point near the front | 4 | 20 |

I also printed a scaling table.  Each time the list grew 10x, linear search did 10x the work while binary search added only 3 or 4 probes, closely tracking log2(n):

| n | Linear (worst) | Binary (worst) | log2(n) |
|---|---|---|---|
| 10 | 10 | 4 | 3.3 |
| 1,000 | 1,000 | 10 | 10.0 |
| 1,000,000 | 1,000,000 | 20 | 19.9 |
## Edge Cases Tested

1. **Empty list:** both returned `-1` with zero comparisons.  In binary search, `high` started at `-1`, so the loop never ran.
2. **Missing values below the smallest and above the largest:** both returned `-1`.  Linear search still checked all 12 alarms, while binary search fell off the left or right end in 3 or 4 probes.
3. **Duplicates:** for a "chattering" alarm that appeared three times, linear search returned the first copy (index 1) and binary search returned the copy its middle probe happened to land on (index 2).  Both answered "is it here?" correctly, but only `first_at_or_after()` reliably found the first copy.
4. **Unsorted input:** binary search returned `-1` for an alarm that **was** in the list.  Its first probe saw a smaller value and threw away the half that actually held the target.  There was no error and no warning.  This was the clearest demonstration of when binary search can't be used.

## Real-World Scenario: Post-Trip Sequence of Events Log

I generated a 5,007-event SOE log (a fixed random seed keeps the output repeatable) with a scripted reactor trip buried in it.  The recorder appends events as they happen, so the log comes out in time order for free.

- **Question A, what alarmed from T+0 to T+0.5 s?**  Time was the sort key, so `first_at_or_after()` found the start of the window in **12 probes** (index 2,453) and the program read forward from there.  It skipped the roughly 2,450 earlier events entirely.
- **Question B, when did feedwater flow low (3300) first alarm?**  The point-number column was in time order, not number order, so binary search was not usable.  Linear search read forward from the earliest event and found the first occurrence at **T−1.850 s** after 2,444 comparisons.  Because it scans in time order, its first match was also the earliest one.  Sorting the log by point number first would have cost a full sort to answer a single question.  The "first-out" alarm came almost two seconds before the trip, which is exactly what a post-trip review is looking for.
- To prove the point, the program also ran `binary_search()` on the unsorted point column.  It returned `-1` even though 3300 appeared in the log twice.

## Real-World Interpretation

Binary search is the right choice when the data is sorted on the key you're searching and you'll search it many times.  Examples are a procedure index, a phone's contact list, or a dictionary.  Linear search is still the right choice when the data is unsorted or sorted by something else, when the list is small, when you'll only search it once, or when you need the earliest match in a log kept in time order.  Binary search can't be used at all when the data isn't sorted on the search key, when the values can't be put in a consistent order, or when there's no fast way to jump to the middle element (a linked list, for example, has to walk node by node to get there).

## Discussion Board Reflection

The biggest thing I learned was that "sorted" isn't a property of a list by itself.  It depends on what you are searching for.  My SOE log was in perfect time order, so binary search found the start of the post-trip window in 12 probes.  By point number, though, the same log was effectively random.  Counting comparisons also made Big-O concrete.  Going from 1,000 to 1,000,000 points multiplied linear search's work by 1,000 and added only 10 probes to binary search.

My main challenge was the duplicates edge case.  Binary search returned index 2 for the repeated alarm while linear search returned index 1, and at first I thought I had a bug.  Tracing it by hand showed both answers were valid.  Binary search just stops on whichever copy the middle lands on.  I wrote `first_at_or_after()` for when I needed the first copy.

I would use binary search when data is sorted on the search key and searched many times.  I would use linear search when data is unsorted, small, or searched once, because sorting it first can cost more than the search saves.
