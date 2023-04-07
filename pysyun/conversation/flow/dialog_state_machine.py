import re

from graphviz import Digraph

from pysyun.conversation.flow.redux import Store
from Levenshtein import distance


def similarity_percentage(str1, str2):
    lev_distance = distance(str1, str2)
    percentage = ((max(len(str1), len(str2)) - lev_distance) / max(len(str1), len(str2))) * 100
    return percentage


class DialogStateMachine:

    def __init__(self, initial_state_pointer, state_nodes):

        self.graph = state_nodes

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

            from_user = action["update"]["message"]["from_user"]

            # Initial state for new negotiators
            if from_user["id"] not in state:
                state[from_user["id"]] = {
                    'observations': [],
                    'pointer': initial_state_pointer
                }

            for node in filter(lambda item: item.identifier == state[from_user["id"]]['pointer'], state_nodes):
                edge = node.edge(text)
                if None is not edge:

                    if None is not node.on_transition:
                        await node.on_transition(action)

                    # Next state after the transition
                    state[from_user["id"]] = {
                         'observations': state[from_user["id"]]['observations'] + [action],
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
            label = node.regex if node.regex and node.regex is not "8---" else node.example
            g.edge(str(node.identifier), str(node.to_state), label=label)

        return g.source


class DialogStateNode:

    def __init__(self, identifier, to_state, example, regex, on_transition):
        # TODO: Probably, need rename to "from_state"
        self.identifier = identifier
        self.to_state = to_state
        self.example = example
        self.regex = regex
        self.on_transition = on_transition

    def edge(self, action):

        if re.match(self.regex, action):
            return self.to_state
        else:
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

    def to(self, to_state, example, matcher=r'8---', on_transition=None):
        self.nodes.append(DialogStateNode(self.current_state, to_state, example, matcher, on_transition))
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
