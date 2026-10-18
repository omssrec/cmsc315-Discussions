# Unit 1 Discussion: Python OOP, Namespaces, and Copying

## Overview

This assignment explored object-oriented programming (OOP) concepts in Python, including inheritance, namespaces, and object copying.

## Implementation Summary

I modeled a nuclear plant scenario, since it ties directly into the operator training program I build at work. `PressurizedWaterReactor` is the parent class: it carries a shared `fuel_type` class variable, `number_of_loops` and `MW_output` instance variables, a constructor, and a `describe()` method that summarizes the reactor. `AP1000Reactor` is the child class: it inherits from `PressurizedWaterReactor`, adds a `containment_type` class variable, two new instance variables (`plant_name`, `startup_year`), a new `activate_passive_cooling()` method, and overrides `describe()` to extend the parent's summary with AP1000-specific details via `super()`.

`demonstrate_namespaces()` creates two `AP1000Reactor` objects, reads `containment_type` through both the class and an instance, adds a `location` attribute to only one reactor, and prints each object's `__dict__` to show that instance namespaces are independent even though the class namespace is shared.

`demonstrate_copying()` creates a reactor with a mutable `sensor_readings` list, then makes a shallow copy with `copy.copy()` and a deep copy with `copy.deepcopy()`. After appending a new reading to the original's list, the shallow copy's readings changed too (it still points at the same list object), while the deep copy's readings stayed untouched (it got its own independent list).

As an extension I created, I added a refueling tracker to `AP1000Reactor`: a `refuel_count` instance variable initialized to 0 in the constructor, and a `refuel()` method that increments the count each time it's called and returns a status message. `main()` demonstrates this by calling `refuel()` twice on a reactor and printing the running total.

## Discussion Board Reflection

To complete this assignment I had to understand and work with how Python separates class namespaces from instance namespaces: a class variable like `containment_type` lives in one shared namespace, while each object's own attributes live in its own `__dict__`, which is why adding `location` to one reactor never affected the other.  The biggest challenge was keeping track of which structural level I was working in - whether an edit belonged inside the class definition, inside `__init__`, or inside `main()` - since Python relies entirely on indentation to convey that, and a method pasted at the wrong level either breaks silently (floats outside the class) or gets masked by a later duplicate definition. 

The copying demonstration highlighted a related distinction: I initially expected `copy.copy()` to fully isolate the new object, but a shallow copy only duplicates the top-level object, so the nested `sensor_readings` list stayed shared between the original and the copy; only `deepcopy()` recursively copied it.  Compared to procedural programming, OOP bundles data and behavior together, so `AP1000Reactor` could extend `PressurizedWaterReactor` without touching already-tested code, which procedural duplication makes harder to achieve safely.  That inheritance-driven reuse pays off in maintainability as a codebase grows, though it does add some structural overhead and indirection compared to a short procedural script - a trade-off that is worthwhile once an application needs to scale or be maintained by more than one developer over time.
 
