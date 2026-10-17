"""
===========================================================
Unit 1 DISCUSSION: Python OOP, Namespaces, and Copying
===========================================================

INSTRUCTIONS:
In this assignment, you will build and explore object-oriented programming (OOP) concepts in Python.
You are provided with starter code containing TODO sections. Your task is to complete, modify, and
analyze the code to demonstrate understanding of inheritance, namespaces, and object copying.
"""


from copy import copy, deepcopy


# TODO 1:
# Create a parent class.
#
# Requirements:
# - Include at least one class variable.
# - Include at least two instance variables.
# - Include a constructor (__init__).
# - Include a method that returns or displays information about the object.

class ReactorComponent:
    """Generic component in a nuclear training simulator."""

    facility_name = "UMGC Training Simulator"  # class variable shared by every component

    def __init__(self, component_id, status="Standby"):
        self.component_id = component_id  # instance variable
        self.status = status               # instance variable

    def get_status_report(self):
        return f"[{self.component_id}] Facility: {self.facility_name} | Status: {self.status}"


# TODO 2:
# Create a child class that inherits from the parent class.
#
# Requirements:
# - Use inheritance.
# - Add at least one new class variable.
# - Add at least two new instance variables.
# - Add at least one new method.
# - Override a method from the parent class.

class Pump(ReactorComponent):
    """Reactor coolant pump. Inherits from ReactorComponent."""

    total_pumps = 0  # new class variable - counts every pump created

    def __init__(self, component_id, flow_rate_gpm, pump_type, status="Standby"):
        super().__init__(component_id, status)
        self.flow_rate_gpm = flow_rate_gpm  # new instance variable
        self.pump_type = pump_type          # new instance variable
        Pump.total_pumps += 1

    def adjust_flow_rate(self, new_rate):
        """New method. Also handles an edge case: rejects a negative flow rate."""
        if new_rate < 0:
            raise ValueError(f"Flow rate cannot be negative: {new_rate}")
        self.flow_rate_gpm = new_rate
        self.status = "Running" if new_rate > 0 else "Standby"

    def get_status_report(self):  # overrides ReactorComponent.get_status_report
        base = super().get_status_report()
        return f"{base} | Pump Type: {self.pump_type} | Flow Rate: {self.flow_rate_gpm} gpm"


# TODO 3:
# Create a function that demonstrates class namespaces and instance namespaces.

def demonstrate_namespaces():
    print("\n=== Namespace Demonstration ===")
    pump_a = Pump("RCP-A", 4200, "Centrifugal")
    pump_b = Pump("RCP-B", 4100, "Centrifugal")

    # Access a class variable through the class itself
    print(f"Access through the class:    Pump.total_pumps = {Pump.total_pumps}")
    # Access the same class variable through an object
    print(f"Access through an instance:  pump_a.total_pumps = {pump_a.total_pumps}")

    # Add a new attribute to only one object after it is created
    pump_a.last_inspection = "2026-09-15"

    # Display each object's namespace using __dict__
    print(f"\npump_a.__dict__: {pump_a.__dict__}")
    print(f"pump_b.__dict__: {pump_b.__dict__}")
    print("(pump_a carries last_inspection; pump_b does not, since it was set on the instance,")
    print(" not the class - each object keeps its own namespace in its own __dict__.)")

    # Display information about the class namespace
    class_methods = [k for k, v in Pump.__dict__.items() if callable(v)]
    print(f"\nPump class namespace: total_pumps={Pump.__dict__['total_pumps']}, "
          f"methods defined directly on Pump={class_methods}")


# TODO 4:
# Create a function that demonstrates shallow copying and deep copying.

def demonstrate_copying():
    print("\n=== Copy Demonstration ===")
    original = Pump("RCP-C", 4300, "Centrifugal")
    original.sensor_log = [98.6, 99.1, 97.8]  # nested mutable data

    shallow = copy(original)
    deep = deepcopy(original)

    # Modify the original object's nested data
    original.sensor_log.append(150.0)  # simulate a new spike reading
    original.flow_rate_gpm = 0

    print(f"Original:  flow_rate={original.flow_rate_gpm}, sensor_log={original.sensor_log}")
    print(f"Shallow:   flow_rate={shallow.flow_rate_gpm}, sensor_log={shallow.sensor_log}")
    print(f"Deep:      flow_rate={deep.flow_rate_gpm}, sensor_log={deep.sensor_log}")

    # copy.copy() only duplicates the top-level object: flow_rate_gpm (an immutable int)
    # looks "frozen" at copy time because reassigning original.flow_rate_gpm just points
    # original to a new int - it doesn't touch shallow's own flow_rate_gpm. But sensor_log
    # (a mutable list) is still the SAME list object in both original and shallow, so the
    # append() shows up in both. deepcopy() recursively copies nested objects too, so deep's
    # sensor_log is a fully independent list and is unaffected by the original's append.
    print("\nNote: the shallow copy's sensor_log changed with the original because copy.copy()")
    print("only duplicates the top-level object - nested mutable objects stay shared.")
    print("deepcopy() recursively copies nested objects, so the deep copy stays independent.")


# TODO 5:
# Complete the main function.

def main():
    print("=== Unit 1 OOP Assignment ===")

    reactor = ReactorComponent("CTRL-01", status="Monitoring")
    print("\nParent object:")
    print(reactor.get_status_report())

    pump = Pump("RCP-D", 4000, "Centrifugal")
    print("\nChild object (inheritance in action):")
    print(pump.get_status_report())
    pump.adjust_flow_rate(4250)
    print(f"After adjust_flow_rate(4250): {pump.get_status_report()}")

    # Student-created extension: exercise the edge-case handling in adjust_flow_rate()
    try:
        pump.adjust_flow_rate(-10)
    except ValueError as e:
        print(f"Edge case handled: {e}")

    demonstrate_namespaces()
    demonstrate_copying()


if __name__ == "__main__":
    main()
