Web VPython 3.2
# This project is a simulation of a hotdog cooker.
# We define a circuit element to be a hotdog, battery, resistor, capacitor.

# To begin, there are given presets that the user can choose from.
# From there, the user can begin the simulation by clicking on the 'Turn on Battery' button.
# The user can look at the specific non-prefixed value of and current through a circuit element by clicking on it.
# For a hotdog, clicking on it will also show its temperature.
# A clicked on element will be indicated by a glow.

# The user can also modify the circuit.
# For all circuit elements excluding the hotdog, the user can modify their respective voltage, resistance, and capacitance by clicking on the object and typing the non-prefixed value.
# To modify a hotdog's radius and length, click on it and use the sliders.
# To remove a circuit element just drag it away from the circuit.
# To add a circuit element:
#     1. Check the 'Attatch to Circuit' box (Note: To end the addition sequence, uncheck the box).
#     2. Click on a circuit element outside the circuit to add. Selected items will have a glow and be see through.
#     3. Click on a or group of circuit element(s) inside the circuit to to be in series or parallel with the added circuit element. Press the 'a' key to end the selection place.
#     4. Specify if it is a series('SERL') addition or a parallel('PARL') addition through the text prompter. Type 'EXIT' in order to return to select more elements to add the circuit element relative to. Selected items will have a glow and be see through.
# During the addition sequence, the user cannot turn on or off the battery, modify any elements, or remove any elements.
# The user is limited to circuits only having at most two batterys and one capacitor.

# To create a hotdog outside of the circuit, click on the 'Create!' button.
# For other elements, the strategy to create a new one is to choose a preset with the element and drag it out.

# While the battery is on, the user cannot modify, remove(except in a special case we'll get into), or add any elements.
# While the battery is on, clicking on a circuit element will also show a graph of the current through it.
# For a hotdog, a graph of its temperature will also appear.
# A hotdog has five stages: uncooked, undercooked, perfect, charred, and burnt. The hotdog will change it's look accordingly.
# The user can remove hotdogs from the circuit by dragging it out. This will not modify the circuit structure.
# The user can reattatch hotdogs by dragging a hotdog nearby an empty section of the circuit.
# To end the simulation, click the 'Turn off Battery' button.
