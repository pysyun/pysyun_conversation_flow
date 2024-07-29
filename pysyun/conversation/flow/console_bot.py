import asyncio
from pysyun.conversation.flow.dialog_state_machine import DialogStateMachineBuilder


class ConsoleBotContext:

    __items = {}

    def __init__(self, bot):
        self.bot = bot

    def add(self, name, value):
        self.__items[name] = value

    def get(self, name):
        return self.__items[name]


class ConsoleBot:

    def __init__(self, token, initial_state="/start", scheduler=None):
        self.state_machine = self.build_state_machine(DialogStateMachineBuilder(initial_state=initial_state)).build()

        if scheduler:
            self.scheduler = scheduler
            scheduler.start(None, self.state_machine)

    def build_state_machine(self, builder):
        return builder

    @staticmethod
    def build_message_response_transition(message):
        async def transition(action):
            print(action)
            print(message)

        return transition

    @staticmethod
    def build_menu_response_transition(title, menu_items):
        async def transition(action):
            # print(action)
            print(title)
            print(menu_items)

        return transition

    def build_graphviz_response_transition(self):
        async def transition(action):
            # print(action)
            print(self.state_machine.to_graphviz())

        return transition


    async def __process_user_input(self, user_input):

        await self.state_machine.process({
            "update": {
                "effective_chat": {
                    # Consider that the console is identified by a constant chat identifier
                    "id": 0,
                    # Consider that all console chats are private
                    "type": "private"
                },
                "message": {
                    "from_user": {
                        # Consider that the console user is constant
                        "id": 0
                    }
                }
            },
            "text": user_input,
            "context": ConsoleBotContext(self)
        })

    async def send_message(self, chat_id, text, reply_markup=None):
        print(text)
        if None is not reply_markup and "keyboard" in reply_markup:
            print(reply_markup["keyboard"])

    async def on_command(self):

        await self.__process_user_input("/start")

        while True:
            user_input = await asyncio.get_event_loop().run_in_executor(None, input)
            await self.__process_user_input(user_input)

    def run(self):
        asyncio.run(self.on_command())
