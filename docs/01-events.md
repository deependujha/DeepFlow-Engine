# Events in PyGame

- In Pygame, an event is `an action that occurs in the system`, such as a user pressing a key, clicking the mouse, moving the mouse, or closing the window.
- These **`events are collected by the operating system and placed into a queue, which the Pygame program can then access and respond to in its main loop`**.

```python
# Cycles through all events occurring
for event in pygame.event.get():
    if event.type == QUIT:
        pygame.quit()
        sys.exit()

    if event.type == INC_SPEED:
        SPEED += 0.5
```

______________________________________________________________________

## Creating custom events

Follow a three-step process:

- define a unique event ID,
- create an Event object,
- and then post it to the Pygame event queue.

```python
# Step 1: Define a unique event ID
MY_CUSTOM_EVENT = pygame.USEREVENT + 1
# Alternatively, Use custom_type() to get a unique ID for your event
MY_CUSTOM_EVENT = pygame.event.custom_type()
```

```python
# Create an event object by passing event ID and custom arbitrary data as a dictionary
custom_event = pygame.event.Event(MY_CUSTOM_EVENT, {'message': 'Hello, world!', 'value': 100})
```

```python
# Post the event to the Pygame event queue
pygame.event.post(custom_event)
```

### Complete code for creating and posting a custom event:

```python
import pygame

MY_CUSTOM_EVENT = pygame.event.custom_type()

custom_event = pygame.event.Event(MY_CUSTOM_EVENT, {'message': 'Hello, world!', 'value': 100})

pygame.event.post(custom_event)
```

### Responding to the custom event in the main loop:

```python
# Inside your main game loop:
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    elif event.type == MY_CUSTOM_EVENT:
        print(f"Received custom event: {event.message} with value {event.value}")
        # Add your custom logic here
```

______________________________________________________________________

## Automating Custom events with Timers

- To have a custom event occur automatically at regular time intervals (e.g., a "poison" effect in an RPG, or a recurring game tick), you can use `pygame.time.set_timer()`.
- This method takes the `event ID` and the `interval in milliseconds` as parameters and posts the event repeatedly without manual intervention.

```python
# Define a unique event ID for the timer
MY_CUSTOM_TIMER_EVENT = pygame.event.custom_type()

# Set a timer to post MY_CUSTOM_TIMER_EVENT every 2000 milliseconds (2 seconds)
pygame.time.set_timer(MY_CUSTOM_TIMER_EVENT, 2000)

# To stop the timer, call it again with the same event ID and a time of 0
pygame.time.set_timer(MY_CUSTOM_TIMER_EVENT, 0)
```

### Responding to the timer event in the main loop:

```python
for event in pygame.event.get():
    if event.type == MY_CUSTOM_TIMER_EVENT:
        print("Timer event triggered!")
        # Add your timer-related logic here
```
