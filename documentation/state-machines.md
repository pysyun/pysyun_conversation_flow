# A beginner's guide to state machines in Python

A state machine is a system that can have multiple states, and defined transitions between those states based on events or conditions. 

For example, think of a traffic light. It can be in one of three states - red, yellow, or green. It transitions between these states based on timers or other logic.

## Why Use a State Machine?

State machines are useful for modeling systems that have complex behavioral logic based on different states. For example:

- Traffic lights
- Order fulfillment flows 
- Conversational bots
- Game character AI
- Protocol/network state tracking

Using an explicit state machine makes this stateful logic easier to understand and maintain.

## Defining States

In Python, states can be represented by simple strings, classes, enums, or any object. For example:

```python
RED = "red"
YELLOW = "yellow" 
GREEN = "green"
```

Or with an Enum:

```python 
from enum import Enum

class TrafficLightState(Enum):
    RED = 1
    YELLOW = 2 
    GREEN = 3
```

## Defining Transitions

The logic for transitioning between states lives outside of the states themselves. This is usually defined with a state machine handler class. 

For example:

```python
# Traffic light controller 
class TrafficLightController:

    def __init__(self):
        self.state = TrafficLightState.RED 

    def timer_expired(self):
        if self.state == TrafficLightState.RED:
           self.state = TrafficLightState.GREEN
        elif self.state == TrafficLightState.YELLOW:
            self.state = TrafficLightState.RED

    # Other transition triggers  
    def pedestrian_pressed(self): 
        ...
```

Transitions can also call action methods before changing state when useful.

## Conversational Bots Example 

State machines are very useful for managing conversational bot flows. 

For example:

```python
class PizzaOrderBot:
    
    # Define states
    START = "START" 
    CHOOSE_PIZZA =  "CHOOSE_PIZZA"
    
    # Bot constructor 
    def __init__(self):
       self.state = self.START

    # Transitions     
    def received_message(self, message):
        if self.state == self.START:
            if message == "start order":
                self.reply("what pizza do you want?")   
                self.state = self.CHOOSE_PIZZA

        elif self.state == self.CHOOSE_PIZZA:
             self.add_to_order(message)
             self.state = self.START
```

This allows managing complex conversational flows in clean, maintainable code!
