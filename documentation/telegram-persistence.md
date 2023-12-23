# Telegram Bot Persistence

The `PersistentTelegramBot` class allows saving and restoring state across bot restarts. This is useful for:

- Preserving user conversation history
- Resuming long running conversations after crashes
- Maintaining user data like profiles or orders

## How it Works

`PersistentTelegramBot` builds on top of the normal `TelegramBot` class. The key addition is a persistence layer backed by a [pickle](https://docs.python.org/3/library/pickle.html) file specified on initialization:

```python
PersistentTelegramBot(
    token="token",
    persistence_file="data.pickle"
)
```

On boot, state is loaded from this file. As users interact, the latest state is periodically saved out.

The file contains a Python dictionary that maps:

```
user_id -> {
   "observations": [messages]
   "pointer": current_state 
} 
```

So the full conversation history and current state is stored per user. 

## Usage Tips

- Schedule periodic saves for better crash resilience  
- Prune old users if file size gets too big
- Make sure one bot instance accesses the file at a time  

This simple persistence approach saves a ton of user annoyance from losing progress in conversations. Give it a try on your next Telegram bot!
