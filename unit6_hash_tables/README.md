# Unit 6 Discussion: Dictionaries as Hash Tables

## Overview

This assignment uses Python dictionaries to demonstrate hash table behavior.

## Learning Objectives

- Insert key-value pairs
- Retrieve values efficiently
- Update existing values
- Remove entries
- Understand hashing concepts

## Requirements

1. Create and populate a dictionary.
2. Demonstrate lookup operations.
3. Demonstrate update operations.
4. Demonstrate delete operations.
5. Test edge cases.
6. Create a real-world scenario.

Scenario: Radiation Worker Dose Lookup

This week I used radiation protection at a plant. Every worker going into the radiologically controlled area (RCA) wears a dosimeter badge. When the badge is scanned at the access point, the system has to pull that worker's year-to-date dose immediately and compare it to the administrative limit. Badge ID → dose (mrem) is a natural key-value pair, and nobody wants to wait at the turnstile while a computer reads through every worker on site. All badge IDs and doses are invented.

How I Implemented It
Insert: created an empty dict and added five badges. The comments explain that Python hashes each key to choose a slot, which is why keys have to be unique and immutable.
Lookup: scanned two badges and printed each worker's dose and remaining margin to the 2,000 mrem admin limit. A lookup hashes the key again and jumps straight to the slot, so it's O(1) on average.
Update: a worker exits after a job with +95 mrem. Assigning to an existing key replaces only the value, so the table still has 5 workers. The update pushed that worker within 10% of the limit, which triggers a supervisor notice.
Delete: a contract worker turns in a badge at the end of the outage, and del removes the entry.
Hashing and collisions (my addition): a simple teaching hash (sum of character codes mod 8) shows RW-1042 and RW-1024 landing in the same slot. I used it instead of Python's hash() because string hashes are randomized every run, and I wanted repeatable output.
Edge Cases Tested
Missing key lookup: get() returns None for an unknown badge instead of raising KeyError. I used None rather than 0 on purpose, because a new hire really does have 0 mrem, and an unknown badge shouldn't look like a real worker.
Deleting a missing key: pop(key, None) returns None and leaves the table alone, where del would crash.
Updating a missing key: plain assignment silently creates a new record. A mistyped badge (RW-4150 for RW-4105) would get its own dose history, so the code checks with in before updating.
Empty dictionary: len() is 0, the dict is falsy, and get() still works.
Real-World Interpretation

Hash tables fit any system where you look things up by a unique ID and need the answer right away: access control, dose tracking, parts and tool crib lookups, user accounts, and caches. They're a poor fit when you need the data in sorted order or need range queries ("everyone above 1,500 mrem"), since the slots have no meaningful order.

Discussion Board Reflection

This assignment helped me connect the dictionary syntax I already use to what is happening underneath. Every insert, lookup, update, and delete starts by hashing the key to find a slot, which is why the cost doesn't grow with the number of workers.

My challenge was the "update a missing key" edge case. I expected an error, but dose_table["RW-4150"] = 20 just created a new worker. In a dose tracking system that's a real problem, because the dose ends up on a record nobody is watching. I fixed it by checking with in before updating, and I used get() and pop() with defaults for the other missing-key cases.

A hash table runs each key through a hash function to get a slot number and stores the value there. A collision happens when two keys land in the same slot. My demo showed RW-1042 and RW-1024 colliding. Python handles collisions by probing for another open slot and resizes the table as it fills. Because lookups go straight to a slot instead of scanning, they average O(1) compared with O(n) for a list.
