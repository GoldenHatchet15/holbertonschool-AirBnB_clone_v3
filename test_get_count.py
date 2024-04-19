#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

# Print counts of all objects and specifically State objects
print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

# Retrieve all State objects as a list
states = list(storage.all(State).values())

# Check if there are any states in the list before proceeding
if states:
    first_state_id = states[0].id  # Get ID of the first State object
    first_state = storage.get(State, first_state_id)  # Get the first State object
    print("First state: {}".format(first_state))
else:
    print("No State objects found.")
