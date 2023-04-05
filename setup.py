from setuptools import setup

setup(
    name='pysyun_conversation_flow',
    version='1.3',
    description='Syun\'s Python SDK for conversation flow control.',
    author='Py Syun',
    author_email='pysyun@vitche.com',
    py_modules=['pysyun_conversation_flow.console_bot', 'pysyun_conversation_flow.dialog_state_machine',
                'pysyun_conversation_flow.redux', 'pysyun_conversation_flow.telegram_bot'],
    install_requires=['asyncio', 'Levenshtein', 'telegram', 'python-telegram-bot', 'graphviz']
)
