"""
===========================================================
UNIT 2 DISCUSSION: STACKS AND QUEUES (PYTHON)
===========================================================

OVERVIEW:
This assignment introduces two fundamental data structures:
the Stack (LIFO) and the Queue (FIFO).

You will complete, modify, and extend the starter code while
explaining key concepts through comments and improved output.
"""

from collections import deque


class Stack:
    def __init__(self):
        # TODO (Student): Create the internal data structure for the stack.
        # Hint: A Python list can be used to store stack values.
        self.items = []

    def push(self, value):
        # TODO (Student): Add value to the stack.
        # Add a short comment explaining why this operation supports LIFO behavior.
        self.items.append(value)
        # append() adds to the END of the list, which we treat as the "top"
        # of the stack.  This is what gives us LIFO: the last item
        # appended is the first one removed.

    def pop(self):
        # TODO (Student): Remove and return the most recently added value.
        # Improve or explain empty-stack handling.
        # What should happen if the stack is empty?
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()
        # list.pop() with no index removes and returns the LAST item,
        # again, the "top" of our stack.  We raise IndexError on an empty
        # stack (mirroring Python's own list behavior) rather than
        # returning None, so a caller can't mistake an empty pop for a
        # legitimate value like 0.

    def peek(self):
        # TODO (Student): Return the top value without removing it.
        # Add a comment explaining what peek does.
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items[-1]
        # Looks at the top item without removing it.  This is useful when you
        # need to know what's next without committing to taking it off.

    def is_empty(self):
        # TODO (Student): Return True if the stack has no values.
        return len(self.items) == 0


class Queue:
    def __init__(self):
        # TODO (Student): Create the internal data structure for the queue.
        # Hint: collections.deque is useful for efficient queue operations.
        self.items = deque()

    def enqueue(self, value):
        # TODO (Student): Add value to the back of the queue.
        # Add a short comment explaining why this operation supports FIFO behavior.
        self.items.append(value)
        # append() adds to the RIGHT (back) of the deque -- new arrivals
        # join the back of the line, which is what gives us FIFO.

    def dequeue(self):
        # TODO (Student): Remove and return the value from the front of the queue.
        # Explain or improve empty-queue handling.
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self.items.popleft()
        # popleft() removes and returns from the LEFT (front) of the
        # deque.  The item that's been waiting longest leaves first.

    def front(self):
        # TODO (Student): Return the front value without removing it.
        # Add a comment explaining what front returns.
        if self.is_empty():
            raise IndexError("front from empty queue")
        return self.items[0]
        # Looks at the front item without removing it.

    def is_empty(self):
        # TODO (Student): Return True if the queue has no values.
        return len(self.items) == 0


def main():
    print("=== UNIT 2: STACKS AND QUEUES ===")
    print("Scenario: Elevator control panel -- floor requests and cancellations\n")

    # ===============================
    # TODO (Student): STACK DEMO
    # ===============================
    # Requirements:
    # 1. Create a Stack object.
    # 2. Add at least 4 values to the stack.
    # 3. Improve the print statements so they clearly explain what is happening.
    # 4. Demonstrate LIFO behavior.
    # 5. Show what happens when pop() is used on an empty stack.
    #
    # Edge Cases:
    # 6. Show what happens when peek() is used on an empty stack.
    # 7. Create a stack with only one item, remove it,
    #    and verify the stack is empty afterward.
    #
    # Scenario: A rider mashes floor buttons, then starts hitting
    # "cancel" -- the elevator controller backs out the MOST RECENT
    # press first, since that's the one still fresh in the queue of
    # intent. This is a stack: last button pressed, first one undone.
    print("=== STACK DEMO: Button-Press Cancellation ===")
    panel = Stack()

    for floor in [5, 12, 3, 8]:
        panel.push(floor)
        print(f"Rider pressed floor {floor}. Top of stack is now: {panel.peek()}")

    print("\nCanceling presses in LIFO order (most recent press undone first):")
    while not panel.is_empty():
        canceled = panel.pop()
        print(f"  Canceled floor {canceled}")

    # Edge case: pop from an empty stack
    print("\nEdge case: canceling again with no pending presses...")
    try:
        panel.pop()
    except IndexError as e:
        print(f"  Handled gracefully: {e}")

    # Edge case: peek at an empty stack
    print("Edge case: checking the top press with nothing pending...")
    try:
        panel.peek()
    except IndexError as e:
        print(f"  Handled gracefully: {e}")

    # Edge case: single-item stack empties out correctly
    print("\nEdge case: single press, then cancel -- stack should empty out")
    panel.push(7)
    print(f"  Pressed floor 7. is_empty() = {panel.is_empty()}")
    panel.pop()
    print(f"  Canceled floor 7. is_empty() = {panel.is_empty()}")

    # ===============================
    # TODO (Student): QUEUE DEMO
    # ===============================
    # Requirements:
    # 1. Create a Queue object.
    # 2. Add at least 4 values to the queue.
    # 3. Improve the print statements so they clearly explain what is happening.
    # 4. Demonstrate FIFO behavior.
    # 5. Show what happens when dequeue() is used on an empty queue.
    #
    # Edge Cases:
    # 6. Show what happens when front() is used on an empty queue.
    # 7. Create a queue with only one item, remove it,
    #    and verify the queue is empty afterward.
    #
    # Scenario: Riders on different floors press the call button.
    # The elevator can't teleport to whoever called last -- it serves
    # requests in the order they came in. This is a queue: first
    # floor to call, first floor served.
    print("\n=== QUEUE DEMO: Elevator Call Dispatch ===")
    dispatch = Queue()

    for floor in [2, 7, 1, 9]:
        dispatch.enqueue(floor)
        print(f"Floor {floor} called the elevator. Front of queue is now: {dispatch.front()}")

    print("\nDispatching in FIFO order (oldest call served first):")
    while not dispatch.is_empty():
        served = dispatch.dequeue()
        print(f"  Elevator arriving at floor {served}")

    # Edge case: dequeue from an empty queue
    print("\nEdge case: dispatching with no pending calls...")
    try:
        dispatch.dequeue()
    except IndexError as e:
        print(f"  Handled gracefully: {e}")

    # Edge case: front of an empty queue
    print("Edge case: checking next call with nothing pending...")
    try:
        dispatch.front()
    except IndexError as e:
        print(f"  Handled gracefully: {e}")

    # Edge case: single-item queue empties out correctly
    print("\nEdge case: single call, then dispatch -- queue should empty out")
    dispatch.enqueue(4)
    print(f"  Floor 4 called. is_empty() = {dispatch.is_empty()}")
    dispatch.dequeue()
    print(f"  Dispatched floor 4. is_empty() = {dispatch.is_empty()}")


if __name__ == "__main__":
    main()
