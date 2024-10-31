from setuptools import setup

setup(
    name='pysyun_conversation_flow',
    version='1.18',
    description='Syun\'s Python SDK for conversation flow control.',
    author='Py Syun',
    author_email='pysyun@vitche.com',
    py_modules=['pysyun.conversation.flow.console_bot', 'pysyun.conversation.flow.dialog_state_machine',
                'pysyun.conversation.flow.redux', 'pysyun.conversation.flow.telegram_bot',
                'pysyun.conversation.flow.persistent_telegram_bot',
                'pysyun.conversation.workers.abandoned_chat_scheduler',
                'pysyun.conversation.workers.cron_scheduler'],
    install_requires=['asyncio', 'Levenshtein', 'telegram', 'python-telegram-bot', 'graphviz', 'APScheduler']
)
