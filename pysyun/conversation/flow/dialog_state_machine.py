import re

from graphviz import Digraph
from Levenshtein import distance

from pysyun.conversation.flow.redux import Store


def similarity_percentage(str1, str2):
    lev_distance = distance(str1, str2)
    percentage = ((max(len(str1), len(str2)) - lev_distance) / max(len(str1), len(str2))) * 100
    return percentage


class DialogStateMachine:

    def __init__(self, initial_state_pointer, state_nodes):

        self.graph = state_nodes

        # Function to change user states
        async def reducer(state, action):
            text = None
            if isinstance(action, str):
                # Just a string
                text = action
            elif "text" in action:
                # An object with a text
                text = action["text"]
            else:
                return state

            from_user = action["update"]["effective_chat"]["id"]

            # Initial state for new negotiators
            if from_user not in state:
                state[from_user] = {
                    'observations': [],
                    'pointer': initial_state_pointer
                }

            for node in filter(lambda item: item.identifier == state[from_user]['pointer'] or item.is_global,
                               state_nodes):

                edge = node.edge(text)
                if None is not edge:

                    if None is not node.on_transition:
                        await node.on_transition(action)

                    # Next state after the transition
                    state[from_user] = {
                         'observations': state[from_user]['observations'] + [action],
                         'pointer': edge
                    }

                    return state
            return state

        self.machine = Store(reducer, {})

    async def process(self, message):
        await self.machine.dispatch_async(message)

    def to_graphviz(self):
        g = Digraph('G')
        for node in self.graph:
            label = node.example
            if label == "8---" or label is None:
                label = node.regex.pattern
            g.edge(str(node.identifier), str(node.to_state), label=label)

        return g.source


class DialogStateNode:

    def __init__(self, identifier, to_state, example, regex, on_transition, is_global=False):
        # TODO: Probably, need rename to "from_state"
        self.identifier = identifier
        self.to_state = to_state
        self.example = example
        self.regex = regex
        self.on_transition = on_transition
        self.is_global = is_global

    def edge(self, action):

        if re.findall(self.regex, action):
            return self.to_state
        if None is not self.example:
            if similarity_percentage(self.example, action) > 50:
                return self.to_state

        return None


class DialogStateMachineBuilder:

    def __init__(self, initial_state=0):
        self.initial_state = initial_state
        self.current_state = initial_state
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)
        self.current_state = node.identifier
        return self

    def to(self, to_state, example, matcher=r'8---', on_transition=None, is_global=False):
        self.nodes.append(DialogStateNode(self.current_state, to_state, example, matcher, on_transition, is_global))
        self.current_state = to_state
        return self

    def edge(self, from_state, to_state, example, matcher=r'8---', on_transition=None):
        self.nodes.append(DialogStateNode(from_state, to_state, example, matcher, on_transition))
        self.current_state = from_state
        return self

    def go(self, example, matcher=r'8---', on_transition=None):
        self.nodes.append(DialogStateNode(self.current_state, self.current_state + 1, example, matcher, on_transition))
        self.current_state = self.current_state + 1
        return self

    def build(self):
        machine = DialogStateMachine(self.initial_state, self.nodes)
        return machine
