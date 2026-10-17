# Unit 1 Discussion: Python OOP, Namespaces, and Copying

## Overview

This assignment explored object-oriented programming (OOP) concepts in Python, including inheritance, namespaces, and object copying.

## Learning Objectives

- Create parent and child classes
- Use inheritance to extend functionality
- Understand class and instance namespaces
- Demonstrate shallow and deep copying
- Apply object-oriented design principles

## Implementation Summary

I modeled a nuclear plant training-simulator scenario, since it ties directly into the operator training program I build at work. `ReactorComponent` is the parent class: it carries a shared `facility_name` class variable, `component_id` and `status` instance variables, a constructor, and a `get_status_report()` method. `Pump` is the child class: it inherited from `ReactorComponent`, added a `total_pumps` class variable (a running count of every pump created), two new instance variables (`flow_rate_gpm`, `pump_type`), a new `adjust_flow_rate()` method, and overrode `get_status_report()` to append pump-specific details to the parent's report.

`demonstrate_namespaces()` created two `Pump` objects, read `total_pumps` through both the class and an instance, added a `last_inspection` attribute to only one pump, and printed each object's `__dict__` to show that instance namespaces are independent even though the class namespace is shared.

`demonstrate_copying()` created a pump with a mutable `sensor_log` list, then made a shallow copy with `copy.copy()` and a deep copy with `copy.deepcopy()`. After appending a new reading to the original's log, the shallow copy's log changed too (it still points at the same list object), while the deep copy's log stayed untouched (it got its own independent list).

As a student-created extension, I added input validation to `adjust_flow_rate()`: it raises a `ValueError` on a negative flow rate, and `main()` demonstrates that edge case being caught.

## Requirements

Complete all TODO sections in the source code:

1. Create a parent class.
2. Create a child class using inheritance.
3. Demonstrate class and instance namespaces.
4. Demonstrate shallow and deep copying.
5. Create and test objects in `main()`.
6. Add a student-created extension.

## Discussion Board Reflection

Completing this assignment reinforced how Python separates class namespaces from instance namespaces: a class variable like `total_pumps` lives in one shared namespace, while each object's own attributes live in its own `__dict__`, which is why adding `last_inspection` to one pump never affected the other. The biggest challenge was the copying demonstration - I initially expected `copy.copy()` to fully isolate the new object, but a shallow copy only duplicates the top-level object, so the nested `sensor_log` list stayed shared between the original and the copy; only `deepcopy()` recursively copied it. Compared to procedural programming, OOP bundles data and behavior together, so `Pump` could extend `ReactorComponent` without touching already-tested code, which procedural duplication makes harder to achieve safely. That inheritance-driven reuse pays off in maintainability as a codebase grows, though it does add some structural overhead and indirection compared to a short procedural script - a trade-off that is worthwhile once an application needs to scale or be maintained by more than one developer over time.
