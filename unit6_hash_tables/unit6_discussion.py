
"""
====================================================
UNIT 6 DISCUSSION: Python Dictionaries as Hash Tables
====================================================
 
INSTRUCTIONS:
In this activity, you will work with Python dictionaries
to simulate the behavior of a hash table.
 
You will modify the provided starter code to demonstrate
common operations and explain key concepts.
 
Follow all TODO prompts in the code and ensure your output
clearly communicates what your program is doing at each step.
 
----------------------------------------------------
SCENARIO: RADIATION WORKER DOSE LOOKUP
Every worker who enters the radiologically controlled area (RCA)
wears a dosimeter badge.  At the access point, the badge ID is
scanned and the system has to pull up that worker's year-to-date
dose right away to check it against the administrative limit.
Badge ID -> dose (mrem) is a natural key-value pair, so a dictionary
(hash table) is used.  All badge IDs and dose values are invented.
----------------------------------------------------
"""
 
ADMIN_LIMIT_MREM = 2000   # site administrative limit for the year (invented)
 
 
def show(table, title):
    """Print the dose table one worker per line."""
    print(f"  {title} ({len(table)} workers):")
    if not table:
        print("    (empty)")
    for badge, dose in table.items():
        print(f"    {badge}: {dose:>5} mrem")
 
 
def teaching_hash(key, slots=8):
    """
    A deliberately simple hash for the collision demo: add up the
    character codes and take the remainder.  Python's real hash() is far
    better, and string hashes are randomized each run, so this keeps the
    demo output the same every time.
    """
    return sum(ord(ch) for ch in key) % slots
 
 
def main():
    print("=== UNIT 6: DICTIONARIES AS HASH TABLES ===")
    print("Scenario: radiation worker dose lookup at the RCA access point")
 
    # ===============================
    # TODO (Student): CREATE A HASH TABLE
    # ===============================
    #
    # Requirements:
    # 1. Create an empty dictionary.
    # 2. Add at least 5 key-value pairs.
    # 3. Add comments explaining how a dictionary
    #    behaves like a hash table.
    # 4. Display the contents of the dictionary.
 
    print("\n=== INSERT OPERATIONS ===")
 
    # A Python dict is a hash table.  When a key is added, Python calls
    # hash(key) to get an integer, then uses that number to pick a slot in
    # an internal array.  The value is stored in that slot with the key.
    # Keys must be unique and immutable (strings work well), because the
    # hash has to stay the same for the life of the entry.
    dose_table = {}
    dose_table["RW-1042"] = 310
    dose_table["RW-2217"] = 1185
    dose_table["RW-3380"] = 45
    dose_table["RW-4105"] = 1720
    dose_table["RW-5561"] = 0       # new hire, no dose yet
    show(dose_table, "Dose table after 5 inserts")
 
    # ===============================
    # TODO (Student): LOOKUP OPERATIONS
    # ===============================
    #
    # Requirements:
    # 1. Retrieve at least two existing keys.
    # 2. Clearly display the lookup results.
    # 3. Add meaningful comments to explain how the lookup works.
 
    print("\n=== LOOKUP OPERATIONS ===")
 
    # A lookup hashes the badge ID again, jumps straight to that slot, and
    # confirms the stored key matches with ==.  It does not walk through
    # the other workers, so it takes about the same time with 5 workers
    # or 5,000.  That is O(1) on average, compared with O(n) for a list.
    for badge in ["RW-2217", "RW-4105"]:
        dose = dose_table[badge]
        margin = ADMIN_LIMIT_MREM - dose
        print(f"  Scan {badge}: {dose} mrem YTD, {margin} mrem below the limit")
 
    # ===============================
    # TODO (Student): UPDATE OPERATIONS
    # ===============================
    #
    # Requirements:
    # 1. Update the value associated with an existing key.
    # 2. Display the dictionary before and after the update.
    # 3. Use comments to explain what happens when an existing key is assigned
    #    a new value.
 
    print("\n=== UPDATE OPERATIONS ===")
 
    # RW-4105 exits the RCA after a job and picked up 95 mrem.
    # Assigning to a key that already exists finds the same slot and
    # replaces only the value.  No second entry is created, so the
    # number of workers stays the same.
    show(dose_table, "Before update")
    dose_table["RW-4105"] += 95
    show(dose_table, "After RW-4105 exits with +95 mrem")
    if dose_table["RW-4105"] > ADMIN_LIMIT_MREM * 0.9:
        print("  -> RW-4105 is within 10% of the admin limit; RP supervisor notified")
 
    # ===============================
    # TODO (Student): DELETE OPERATIONS
    # ===============================
    #
    # Requirements:
    # 1. Delete at least one key-value pair.
    # 2. Display the dictionary before and after deletion.
    # 3. Use comments to explain what happens when a key is removed.
 
    print("\n=== DELETE OPERATIONS ===")
 
    # A contract worker (RW-3380) finishes the outage and turns in the
    # badge.  del hashes the key, finds the slot, and removes the entry.
    # Python leaves a "deleted" marker in the slot so later lookups for
    # other keys that collided past this slot still find their way.
    show(dose_table, "Before delete")
    del dose_table["RW-3380"]
    show(dose_table, "After RW-3380 turns in the badge")
 
    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least two edge cases.
    #
    # Example ideas:
    # - Lookup a missing key
    # - Delete a missing key safely
    # - Update a missing key
    # - Use an empty dictionary
    #
    # Explain what happens in each case.
 
    print("\n=== EDGE CASES ===")
 
    # 1) Lookup a missing key.  dose_table["RW-9999"] would raise KeyError
    #    and crash the access point.  get() returns a default instead.
    #    Using None (not 0) matters here: 0 would look like a real worker
    #    with no dose, which is exactly how RW-5561 is stored.
    result = dose_table.get("RW-9999")
    print(f"  1) Lookup unknown badge RW-9999 -> {result} (deny entry, send to RP desk)")
    print(f"     Lookup new hire RW-5561      -> {dose_table.get('RW-5561')} (real worker, 0 mrem)")
 
    # 2) Delete a missing key safely.  del would raise KeyError.
    #    pop() with a default removes the key if it is there and otherwise
    #    returns the default, leaving the table unchanged.
    removed = dose_table.pop("RW-3380", None)
    print(f"  2) Remove RW-3380 a second time -> {removed}, table size still {len(dose_table)}")
 
    # 3) Update a missing key.  This is a quiet trap: += on a missing key
    #    raises KeyError, but plain assignment silently CREATES a new
    #    worker.  A mistyped badge would get its own dose record instead
    #    of updating the real one, so check with "in" first.
    typo = "RW-4150"   # meant RW-4105
    if typo in dose_table:
        dose_table[typo] += 20
    else:
        print(f"  3) Update {typo}: not found, no record created (possible typo of RW-4105)")
 
    # 4) Empty dictionary.  len() is 0, an empty dict is falsy, and get()
    #    still returns the default without an error.
    empty = {}
    print(f"  4) Empty table: len={len(empty)}, bool={bool(empty)}, "
          f"get('RW-1042')={empty.get('RW-1042')}")
 
    # ===============================
    # HASHING AND COLLISIONS (my addition)
    # ===============================
    # With only 8 slots, different keys can land in the same slot.  That
    # is a collision.  RW-1042 and RW-1024 have the same characters in a
    # different order, so this simple hash gives them the same slot.
    # Python resolves collisions by probing for another open slot, and it
    # resizes the table as it fills so collisions stay rare and lookups
    # stay close to O(1).
    print("\n=== HASHING AND COLLISIONS ===")
    slots = {}
    for badge in ["RW-1042", "RW-2217", "RW-4105", "RW-5561", "RW-1024"]:
        slot = teaching_hash(badge)
        note = f"  <- COLLISION with {slots[slot]}" if slot in slots else ""
        slots.setdefault(slot, badge)
        print(f"  {badge} -> slot {slot}{note}")
 
 
if __name__ == "__main__":
    main()
 



if __name__ == "__main__":
    main()
