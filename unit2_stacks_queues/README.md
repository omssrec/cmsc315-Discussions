# Unit 2 Discussion: Stacks and Queues

## Overview

This project implements two fundamental linear data structures, Stack (LIFO) and Queue (FIFO).  As well as demonstrates them through a building elevator control system scenario.

## Scenario: Elevator Control Panel

I modeled an elevator's control logic using both structures:

- **Stack -- button-press cancellation.** When a rider presses several floor buttons and then starts canceling, the controller will back out the *most recently pressed* floor first. That's LIFO: the last action to be input is the first one undone.

- **Queue -- call dispatch.** When different floors call the elevator, it can't skip ahead to whoever called most recently, it serves requests in the order they arrived.  That's FIFO: first floor to call, first floor served.

## Design Notes

- `Stack.pop()` and `Stack.peek()` raise `IndexError` on an empty stack rather than failing silently or returning `None` -- this keeps a legitimate "empty result" from being confused with an actual floor value like `0`.

- `Queue` uses `collections.deque` instead of a list because removing from the front of a list is O(n) (every remaining element has to shift), while `deque.popleft()` is O(1).

## Edge Cases Tested

- Popping/dequeuing from an empty structure (handled via IndexError)
- Peeking/checking front of an empty structure (handled via IndexError)
- A single-item structure correctly reports `is_empty() == True` after its one item is removed

## Discussion Board Reflection

Building this assignment demonstrated how much a data structure's behavior is just a decision about which end you touch.  Stack and queue share almost identical operations (add, remove, look) but swapping `pop()` for `popleft()` is the entire difference between LIFO and FIFO in this control system.  My biggest challenge was rerFalizing I couldn't write generic demo code (push 1, 2, 3, pop) and instead use a scenario concrete enough that the edge cases felt like real situations.  for exmaple canceling a button press you haven't made yet, or an elevator with no pending calls, actually mean something once they're tied to a physical system.  In practice, stacks fit problems where the most recent action matters most (undo, backtracking, call stacks in recursion), while queues fit problems where order of arrival is the whole point (task scheduling, message processing, anything that has to be "fair").
