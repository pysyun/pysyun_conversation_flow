# Implementing State Machine Transition Handlers

The state machines in this project allow defining actions that run when transitioning from one state to another. These are called **transition handlers**.

Transition handlers are passed to state machine builder methods like:

```python
.edge("/start", "/next", "input", on_transition=my_handler)
```

Some common uses for transition handlers are below.

## Sending Bot Messages

To send a message back to the user: 

```python
def send_message(text):
    async def handler(action):
        await action["context"].bot.send_message(
           chat_id = action["update"].message.chat_id,
           text = text
        )
    return handler
```

Usage:

```python 
.edge("/start", "/next", "input", on_transition=send_message("Hello"))  
```

## Updating Persistent User State

To save user data across conversations:

```python
def update_user_state(key, value):
    async def handler(action):
        user_id = action["update"].message.from_user.id 
        db.save(user_id, {key: value})  
    return handler
```

Usage:

```python
.edge("/start", "/next", "input", on_transition=update_user_state("pizzas", 0))
```

## Calling APIs

To integrate external APIs:

```python 
def call_api(endpoint, params):
    async def handler(action):
        requests.get(endpoint, params)
    return handler
```

Usage:

```python
.edge("/start", "/next", "input", on_transition=call_api("/orders", {...}))
```

These allow powerful workflows to be built on state transitions!
