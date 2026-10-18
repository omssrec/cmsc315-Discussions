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
#
# Replace the pass statement with your implementation.

class PressurizedWaterReactor:
    fuel_type = "Enriched Uranium Oxide (UO2)" # class variable

    def __init__(self, number_of_loops, MW_output):
        self.number_of_loops = number_of_loops
        self.MW_output = MW_output

    def describe(self):
        return f"This reactor uses {self.fuel_type} fuel, has {self.number_of_loops} loops, and produces {self.MW_output} MW."


# TODO 2:
# Create a child class that inherits from the parent class.
#
# Requirements:
# - Use inheritance.
# - Add at least one new class variable.
# - Add at least two new instance variables.
# - Add at least one new method.
# - Override a method from the parent class.
#
# Replace the pass statement with your implementation.

class AP1000Reactor(PressurizedWaterReactor):
    containment_type = "Passive" # new class variable

    def __init__(self, number_of_loops, MW_output, plant_name, startup_year):
        super().__init__(number_of_loops, MW_output)
        self.plant_name = plant_name
        self.startup_year = startup_year
        self.refuel_count = 0  # my extension: tracks refueling outages

    def activate_passive_cooling(self):
        return f"Passive containment cooling activated at {self.plant_name}."

    def describe(self):
        base_description = super().describe()
        return f"{base_description} It is an AP1000 at {self.plant_name}, startup year {self.startup_year}, with {self.containment_type} containment."
    
# TODO 6: Student created extension

    def refuel(self):
        """My extension: records a refueling outage."""
        self.refuel_count += 1
        return f"{self.plant_name} has completed refueling outage #{self.refuel_count}."


# TODO 3:
# Create a function that demonstrates class namespaces and instance namespaces.
#
# Your function should:
# - Create at least two objects of the child class.
# - Access a class variable through the class itself.
# - Access the same class variable through an object.
# - Add a new attribute to only one object after it is created.
# - Display each object's namespace using __dict__.
# - Display information about the class namespace.

def demonstrate_namespaces():
    print("\n=== Namespace Demonstration ===")
    reactor1 = AP1000Reactor(2, 1117, "Vogtle Unit 3", 2023)
    reactor2 = AP1000Reactor(2, 1117, "Vogtle Unit 4", 2024)

    # access the class variable through the class itself
    print(f"Class variable via the class: AP1000Reactor.containment_type = {AP1000Reactor.containment_type}")

    # access the same class variable through an object
    print(f"Class variable via an object: reactor1.containment_type = {reactor1.containment_type}")

    # add a new attribute to only one object
    reactor1.location = "Waynesboro, Georgia"

    # display each object's own namespace
    print(reactor1.__dict__)
    print(reactor2.__dict__)

    # display something about the class namespace
    print(f"Class namespace: containment_type = {AP1000Reactor.__dict__['containment_type']}")


# TODO 4:
# Create a function that demonstrates shallow copying and deep copying.
#
# Requirements:
# - Create an object that contains nested mutable data.
# - Create a shallow copy.
# - Create a deep copy.
# - Modify the original object's nested data.
# - Display the original object, shallow copy, and deep copy.
# - Use comments to explain the difference between shallow and deep copying.

def demonstrate_copying():
    print("\n=== Copy Demonstration ===")
    original = AP1000Reactor(2, 1117, "Vogtle Unit 3", 2023)
    original.sensor_readings = ["2300 PSIG", "550 F", "1200 ppm"]  # nested mutable data (a list)

    shallow = copy(original)
    deep = deepcopy(original)

    # modify the original's nested data
    original.sensor_readings.append("605 F")

    print(f"Original sensor_readings: {original.sensor_readings}")
    print(f"Shallow copy sensor_readings: {shallow.sensor_readings}")
    print(f"Deep copy sensor_readings: {deep.sensor_readings}")

    # TODO: add a comment here explaining what you observe and why
    # copy.copy() only duplicates the top-level AP1000Reactor object - the nested
    # sensor_readings list is still the SAME list object in both original and shallow,
    # so appending to original's list shows up in shallow too. deepcopy() recursively
    # copies nested objects, so deep's sensor_readings is a fully independent list
    # and is unaffected by the original's append.


# TODO 5:
# Complete the main function.
#
# Requirements:
# - Create at least one object from the parent class.
# - Create at least one object from the child class.
# - Demonstrate inheritance by calling methods.
# - Call your namespace demonstration function.
# - Call your copy demonstration function.

def main():
    print("=== Unit 1 OOP Assignment ===")

    print("\nParent object:")
    parent_reactor = PressurizedWaterReactor(3, 1000)
    print(parent_reactor.describe())

    print("\nChild object (inheritance in action):")
    child_reactor = AP1000Reactor(2, 1117, "Vogtle Unit 3", 2023)
    print(child_reactor.describe())
    print(child_reactor.activate_passive_cooling())
    
    print("\nStudent-created extension: refueling tracker")
    print(child_reactor.refuel())
    print(child_reactor.refuel())
    print(f"Total refuelings at {child_reactor.plant_name}: {child_reactor.refuel_count}")

    demonstrate_namespaces()
    demonstrate_copying()


if __name__ == "__main__":
    main()






