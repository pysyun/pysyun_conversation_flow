class Store:
    def __init__(self, reducer, initial_state):
        self.state = initial_state
        self.reducer = reducer

    def dispatch(self, action):
        self.state = self.reducer(self.state, action)

    async def dispatch_async(self, action):
        self.state = await self.reducer(self.state, action)
