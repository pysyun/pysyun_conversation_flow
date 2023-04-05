from setuptools import setup

setup(
    name='pysyun_conversation_flow',
    version='1.3',
    description='Syun\'s Python SDK for conversation flow control.',
    author='Py Syun',
    author_email='pysyun@vitche.com',
    py_modules=['console_bot', 'dialog_state_machine',
                'redux', 'telegram_bot'],
    install_requires=['asyncio', 'Levenshtein', 'telegram', 'python-telegram-bot', 'graphviz']
)
