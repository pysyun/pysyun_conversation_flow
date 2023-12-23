# Back-end Redux pattern

In spite of many talks that Redux cannot be used in backend, we use it intensively for particular cases.
The implementation is [here](../pysyun/conversation/flow/redux.py).

The Back-end Redux pattern provides a way to manage state in a backend server application. It is inspired by the Redux library often used in frontend React applications.

The core ideas are:

- **Single source of truth:** The state for the application is stored in a single Store object. All state mutations go through the Store.
- **State is immutable:** The Store state is never mutated directly. Instead new state is returned from reducers. 
- **Changes via dispatch:** New states are produced by dispatching Actions to Reducers. Reducers take the current state and action as input and return the new state.

This creates a predictable, traceable state management architecture.

In this project, the Store is implemented in `redux.py`:

```python
class Store:
    def __init__(self, reducer, initial_state):
        self.state = initial_state
        self.reducer = reducer

    def dispatch(self, action):
        self.state = self.reducer(self.state, action)
```

The key ideas map to:

- `self.state` is the single source of truth
- State is never mutated, only overwritten with new state from reducer
- `dispatch()` sends actions to the reducer 

Async actions are also supported via `dispatch_async()`.

This Store can then be used with reducers and actions to build state machines and other stateful backend systems.
