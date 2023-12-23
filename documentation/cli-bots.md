# Command Line Interface Bots

This project includes a `ConsoleBot` class for building bots that run on the command line interface (CLI). 

## What is a CLI Bot?

A CLI bot allows users to have a conversation by typing text commands into a terminal. The bot listens for user input, sends back text responses, and manages state like a normal chat bot.

CLI bots are useful for:

- Testing chat bots without deploying to a real chat platform 
- Getting direct CLI access to a bot for debugging
- Building bots for CLI-based applications like online RPGs

## Using the ConsoleBot

The `ConsoleBot` wrapper provides an entrypoint that:

- Sets up the command reader to get user input  
- Sends output back to the terminal
- Handles a stub user and chat context

To use it:

```python
from pysyun.conversation.flow.console_bot import ConsoleBot

bot = ConsoleBot("/start")
bot.run()
```

The bot runs until interrupted with Ctrl-C.

## Building a CLI Bot 

To build a custom bot extend the `ConsoleBot` class:

```python
class MyCliBot(ConsoleBot):

    def build_state_machine(self, builder):
        # Define state machine here
        return builder.edge(...) 

bot = MyCliBot() 
bot.run()
```

The state machine is defined the same as any other bot built on this framework. 

Transitions can call `send_message()` on `action["context"].bot` to send output:

```python 
def send_response(text):
    async def transition(action):
       await action["context"].bot.send_message(0, text) 
    return transition
```

See the example [pizza bot](../flows/pizza) CLI implementation for more details.
