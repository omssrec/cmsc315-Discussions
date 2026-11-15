"""
=====================================================
UNIT 5 DISCUSSION: SEARCH ALGORITHMS (LINEAR vs BINARY)
=====================================================

INSTRUCTIONS:
In this assignment, you will implement and analyze two
fundamental search algorithms: linear search and binary search.

You will demonstrate your understanding by modifying the
provided code, running experiments on different dataset sizes,
and clearly explaining your results through code comments
and program output.

SCENARIO: CONTROL ROOM ALARM LOOKUP
When an alarm comes in, an operator has two very different search
problems:
  1. "What does alarm 4410 mean?"  The control operater uses an Alarm Response Procedure (ARP) 
      to respond to his situation.  The ARP index is kept SORTED by alarm point number, so binary search works.
  2. "After the reactor trip, when did point 3300 FIRST alarm?"  The
     Sequence of Events (SOE) log is sorted by TIME, not by point number,
     so for this question only a linear search will work.
The same log is sorted for one question and unsorted for the other.
Whether a list counts as "sorted" depends on what you are searching for.
All alarm numbers, titles, and events are invented for this demo.
"""

import math
import random

def _count(stats):
    """Add one to the probe counter if the caller passed one in."""
    if stats is not None:
        stats["comparisons"] += 1

def linear_search(lst, target, stats=None):
    """
    TODO (Student):
    Implement a linear search algorithm.

    Requirements:
    - Search the list from beginning to end.
    - Return the index if the target is found.
    - Return -1 if the target is not found.
    - Add comments explaining why linear search
      has O(n) time complexity.
    """
    # Linear search assumes nothing about the order of the list.  That is
    # its strength (it works on anything) and its weakness: looking at one
    # element tells us nothing about where the target ISN'T, so the only
    # safe move is to check the next element.
    #
    # Why O(n): in the worst case (target is last or missing) every one of
    # the n elements is checked exactly once.  Double the list and you
    # double the work.  On average a found target takes about n/2 checks,
    # which is still proportional to n.
    #
    # stats is optional and only used to count comparisons for the output.
    for index, value in enumerate(lst):
        _count(stats)
        if value == target:
            return index          # first match wins, so we stop early
    return -1                     # checked all n elements, not here


def binary_search(lst, target stats=None):
    """
    TODO (Student):
    Implement a binary search algorithm.

    Requirements:
    - Assume the list is already sorted.
    - Repeatedly reduce the search space by half.
    - Return the index if the target is found.
    - Return -1 if the target is not found.
    - Add comments explaining how each iteration
      reduces the search space.
    """
    # low and high bracket the only part of the list where the target
    # could still be.  At the start that is the whole list.
    low = 0
    high = len(lst) - 1

    # If low passes high, the bracket is empty and the target is not here.
    # For an empty list, high starts at -1, so the loop never runs.
    while low <= high:
        mid = (low + high) // 2
        _count(stats)             # one probe of the middle element

        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            # The middle is too small.  Because the list is sorted,
            # everything to the LEFT of mid is too small as well, so that
            # whole half is thrown out with one comparison.
            low = mid + 1
        else:
            # The middle is too big, so everything to the RIGHT is too big.
            high = mid - 1

        # Each pass cuts the bracket roughly in half:
        # n -> n/2 -> n/4 -> ... -> 1.  It takes about log2(n) halvings to
        # get down to one element, which is why binary search is O(log n).

    return -1


def first_at_or_after(sorted_lst, target, stats=None):
    """
    Extra helper (my addition): binary search for the FIRST index whose
    value is >= target.  Returns len(sorted_lst) if nothing qualifies.

    Plain binary_search answers "is this exact value here?"  A time-window
    question ("what happened in the 500 ms after the trip?") needs "where
    does this window START?" instead, since there may be no event at that
    exact millisecond.  It still halves the range every pass.
    """
    low, high = 0, len(sorted_lst)
    while low < high:
        mid = (low + high) // 2
        _count(stats)
        if sorted_lst[mid] < target:
            low = mid + 1         # start of window is right of mid
        else:
            high = mid            # mid might be the start, keep it
    return low


def compare(lst, target, label=""):
    """Run both searches on the same list and print them side by side."""
    lin_stats = {"comparisons": 0}
    bin_stats = {"comparisons": 0}
    lin = linear_search(lst, target, lin_stats)
    bin_ = binary_search(lst, target, bin_stats)
    print(f"  {label:<34} linear -> {lin:>7} ({lin_stats['comparisons']:>7,} comparisons)"
          f" | binary -> {bin_:>7} ({bin_stats['comparisons']:>2} probes)")
    return lin, bin_


def fmt_ms(ms_from_trip):
    """Format a time relative to the reactor trip, e.g. T-1.850 s."""
    sign = "+" if ms_from_trip >= 0 else "-"
    return f"T{sign}{abs(ms_from_trip) / 1000:.3f} s"


def main():
    print("=== UNIT 5: SEARCH ALGORITHMS ===")
    print("Scenario: control room alarm lookup")

    # The Alarm Response Procedure (ARP) index, keyed by alarm point
    # number.  Titles are only for readable output.
    arp_titles = {
        1010: "Reactor coolant pump A low flow",
        1025: "Reactor coolant pressure high",
        1140: "Reactor coolant temperature high",
        2030: "Borehole water level low",
        2075: "Casing annulus pressure high",
        3110: "Primary heat exchanger delta-T high",
        3300: "Feedwater flow low",
        4205: "Control rod position deviation",
        4410: "Neutron flux rate high",
        5120: "Wellhead radiation monitor alert",
        6000: "Emergency power not available",
        7350: "Fire detection - control building",
    }
    

    # ===============================
    # TODO (Student): SMALL DATASET
    # ===============================
    #
    # Requirements:
    # 1. Create a small sorted dataset.
    # 2. Test both linear search and binary search.
    # 3. Search for:
    #    - a value that exists
    #    - a value that does not exist
    # 4. Use comments to clearly explain the results.

    print("\n=== SMALL DATASET TEST ===")
    
    # 12 alarm numbers.  sorted() makes the precondition for binary
    # search explicit instead of relying on how the dict was typed.
    arp_index = sorted(arp_titles)
    print(f"  ARP index ({len(arp_index)} alarms): {arp_index}")

    # Exists: alarm 4410 is the 9th entry.  Linear search walks 1010, 1025,
    # ... and needs 9 comparisons.  Binary search probes the middle (3110),
    # sees 4410 is bigger, drops the left half (6 alarms gone in one
    # comparison), and the next middle IS 4410, so it takes 2 probes.
    i, _ = compare(arp_index, 4410, "Lookup 4410 (exists)")
    print(f"    -> ARP for 4410: {arp_titles[arp_index[i]]}")

    # Does not exist: an operator mistypes 4400.  Linear search has to
    # check all 12 alarms before it can say "not here."  Binary search
    # narrows to the gap between 4205 and 4410 and gives up in 4 probes.
    compare(arp_index, 4400, "Lookup 4400 (typo, missing)")

    # Another one: 2075 is in the left half, so it shows the halving
    # going the other direction.  It is only 5th in the list, so linear
    # search (5) and binary search (4) come out nearly even.
    i, _ = compare(arp_index, 2075, "Lookup 2075 (exists)")
    print(f"    -> ARP for 2075: {arp_titles[arp_index[i]]}")

    # At this size the difference is only a few comparisons, so with
    # 12 items either method is fine.

    # ===============================
    # TODO (Student): LARGE DATASET
    # ===============================
    #
    # Requirements:
    # 1. Create a much larger sorted dataset.
    # 2. Test both search algorithms.
    # 3. Compare the results.
    # 4. Use comments to explain why binary search becomes more
    #    efficient as datasets grow larger.

    print("\n=== LARGE DATASET TEST ===")

    # The plant computer's full point database: 1,000,000 point numbers.
    # Using only even numbers (100000, 100002, ...) keeps the list sorted
    # and guarantees that every odd number is a value that is missing.
    n = 1_000_000
    points = list(range(100_000, 100_000 + 2 * n, 2))
    print(f"  Point database: {len(points):,} sorted points "
          f"({points[0]:,} to {points[-1]:,})")

    near_end = points[-5]      # exists, close to the end (bad for linear)
    missing = points[-5] + 1   # odd, so it is not in the list
    near_front = points[3]     # exists, near the front (good for linear)
    compare(points, near_end, f"Find {near_end:,} (near end)")
    compare(points, missing, f"Find {missing:,} (missing)")
    compare(points, near_front, f"Find {near_front:,} (near front)")

    # Why the gap grows: linear search does work proportional to n, binary
    # search does work proportional to log2(n).  Multiplying n by 10 makes
    # linear search 10x slower but adds only about 3.3 probes to binary
    # search.  The table below counts worst-case comparisons (target
    # missing and larger than everything) as the list grows.
    print("\n  Worst-case comparisons as the list grows:")
    print(f"  {'n':>11} | {'linear':>11} | {'binary':>6} | {'log2(n)':>7}")
    print("  " + "-" * 45)
    for size in [10, 100, 1_000, 10_000, 100_000, 1_000_000]:
        data = points[:size]
        target = data[-1] + 1
        ls, bs = {"comparisons": 0}, {"comparisons": 0}
        linear_search(data, target, ls)
        binary_search(data, target, bs)
        print(f"  {size:>11,} | {ls['comparisons']:>11,} | {bs['comparisons']:>6} "
              f"| {math.log2(size):>7.1f}")
    # Binary search's column tracks log2(n): a million items take only
    # about 20 probes because 2^20 is roughly 1,000,000.

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least two edge cases.
    #
    # Example ideas:
    # - Empty list
    # - Single-element list
    # - Value not present
    # - Value at the first position
    # - Value at the last position
    #
    # Explain what happens in each case.

    print("\n=== EDGE CASE TESTS ===")

    # 1) Empty list.  Linear search's loop has nothing to iterate over.
    #    Binary search starts with high = -1, so low <= high is False
    #    right away.  Both return -1 with zero comparisons.
    compare([], 4410, "1) Empty list")

    # 2) Missing values outside the range.  Linear search still has to
    #    check all 12 alarms.  Binary search falls off the left end or the
    #    right end in 3-4 probes.  Both return -1.
    compare(arp_index, 5, "2a) Below smallest")
    compare(arp_index, 9999, "2b) Above largest")

    # 3) Duplicates.  The alarm 2075 shows up three times (it chattered).
    #    Linear search returns the FIRST copy.  Binary search returns
    #    whichever copy it happened to hit in the middle.  Both are
    #    "correct" for "is it here?", but they are not the same answer to
    #    "where is the first one?"  first_at_or_after() fixes that.
    dupes = [1010, 2075, 2075, 2075, 3300]
    compare(dupes, 2075, "3) Duplicates of 2075")
    print(f"    -> first_at_or_after finds the first copy at index "
          f"{first_at_or_after(dupes, 2075)}")

    # 4) Unsorted input breaks binary search, and it does so silently.
    #    4410 IS in this list, but the first probe sees 1010 < 4410 and
    #    throws out the left half, which is where 4410 actually is.  Binary
    #    search returns -1 and gives no error.  This is the main condition
    #    under which binary search cannot be used.
    unsorted_alarms = [4410, 2030, 1010, 7350, 3300]
    compare(unsorted_alarms, 4410, "4) UNSORTED list, 4410 present")

    # ===============================
    # REAL-WORLD SCENARIO (my addition)
    # ===============================
    # Sequence of Events (SOE) log after a reactor trip.  The SOE recorder
    # stamps every alarm with a millisecond time and appends it to the end,
    # so the log is in time order as it is written, at no extra cost.
    # The log is sorted by time.  It is not sorted by point number.

    print("\n=== REAL-WORLD SCENARIO: POST-TRIP SEQUENCE OF EVENTS LOG ===")

    rng = random.Random(315)                  # fixed seed = repeatable output
    trip_ms = 600_000                         # trip 10 minutes into recording
    background_pool = [p for p in arp_index if p not in (3300, 4410)] + list(range(8000, 8040))

    # 5,000 routine background alarms spread over 20 minutes.
    log = [(rng.randint(0, 1_200_000), rng.choice(background_pool)) for _ in range(5_000)]

    # The scripted story of the trip.  Feedwater flow dropped first, then
    # temperature and flux responded, then the reactor tripped.
    script = [
        (trip_ms - 1_850, 3300),   # feedwater flow low (the "first out")
        (trip_ms - 900, 1140),     # coolant temperature high
        (trip_ms - 120, 4410),     # neutron flux rate high
        (trip_ms, 4205),           # rods move on the trip
        (trip_ms + 85, 1025),      # pressure transient
        (trip_ms + 310, 3110),     # heat exchanger dT
        (trip_ms + 47_000, 3300),  # feedwater low again later (a duplicate)
    ]
    log.extend(script)
    log.sort()                     # done by the recorder in real life

    times = [t for t, _ in log]            # the sorted column
    point_column = [p for _, p in log]     # the unsorted column, same indexes
    print(f"  SOE log: {len(log):,} events, sorted by time only")

    # Question A: "What alarmed in the 500 ms after the trip?"
    # Time is the sort key, so binary search finds where the window starts
    # and then we read forward.  No need to scan the ~2,450 events before it.
    window_stats = {"comparisons": 0}
    start = first_at_or_after(times, trip_ms, window_stats)
    print(f"\n  A) Events from T+0 to T+0.5 s  "
          f"(window start found in {window_stats['comparisons']} probes, index {start:,}):")
    j = start
    while j < len(log) and times[j] <= trip_ms + 500:
        t, p = log[j]
        print(f"     {fmt_ms(t - trip_ms)}  {p}  {arp_titles.get(p, 'plant computer point')}")
        j += 1

    # Question B: "When did point 3300 FIRST alarm?"
    # The point column is in time order, not number order, so binary search
    # is not usable here.  Its first probe would compare against a random
    # point number and throw out half the log for no valid reason.  Linear
    # search reads from the earliest event forward, so its first match is
    # also the earliest occurrence.  Sorting the log by point number first
    # would cost a full sort just to answer one question, so a single
    # linear pass is the cheaper choice.
    first_stats = {"comparisons": 0}
    k = linear_search(point_column, 3300, first_stats)
    print(f"\n  B) First occurrence of 3300 ({arp_titles[3300]}): "
          f"{fmt_ms(times[k] - trip_ms)}, log index {k:,}, "
          f"found after {first_stats['comparisons']:,} comparisons")
    print("     -> The first-out alarm came almost 2 seconds before the trip.")

    # Show what goes wrong if someone runs binary search on that column anyway.
    wrong = binary_search(point_column, 3300)
    print(f"     binary_search on the unsorted point column -> {wrong}  "
          f"(wrong: 3300 is in the log)")


if __name__ == "__main__":
    main()
