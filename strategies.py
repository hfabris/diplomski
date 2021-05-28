import random

# class for random strategy
# employees and defender will always have random strategy
# actions and components are chosen randomly
class Random():

    def __init__(self, actions):
        self.actions = actions
        self.last_action = ""

    def chose_action(self):
        action_names = list(self.actions.keys())
        action_weights = list(self.actions.values())

        action_order = []

        while True:
            chosen_action = random.choices(action_names, weights = action_weights, k=1)[0]
            chosen_action_index = action_names.index(chosen_action)
            action_order.append(chosen_action)

            del action_names[chosen_action_index]
            del action_weights[chosen_action_index]

            if action_names == []: break

        return action_order

    def chose_component(self, args):
        list_of_components = args[0]
        return random.choice(list_of_components)

    def update_last_action(self, action):
        self.last_action = action

# class for greedy strategy
# actions are chosen based on greedy algorithm: exfiltrate, enumerate, lateral movement and probe accounts
# rest of actions are chosen randomly
# component is chosen greedy, chose the one with the highest priviledges
class Greedy():

    def __init__(actions):
        self.actions = actions
        self.last_action = ""

    def chose_action(self):
        actions_order = []
        if "exfiltrate_data" in self.actions:
            actions_order.append("exfiltrate_data")
        if "enumerate_host" in self.actions:
            actions_order.append("enumerate_host")
        if "lateral_movement" in self.actions:
            actions_order.append("lateral_movement")
        if "account_discovery" in self.actions:
            actions_order.append("account_discovery")
        other_actions = [x for x in self.actions if x not in actions_order]
        actions_order += random.shuffle(other_actions)
        return actions_order

    def chose_component(self, args):
        list_of_components = args[0]


    def update_last_action(self, action):
        self.last_action = action


# class for finite state machine
# actions are chosen in sequential order, when it reaches the end it starts again from the starts
# component is chosen randomly
class Finite_State_Machine():

    def __init__(self, actions):
        self.actions = []

        if "initial_access" in actions:
            self.actions.append("initial_access")
        if "escalate_priviledges" in actions:
            self.actions.append("escalate_priviledges")
        if "dump_credentials" in actions:
            self.actions.append("dump_credentials")
        if "enumerate_host" in actions:
            self.actions.append("enumerate_host")
        if "exfiltrate_data" in actions:
            self.actions.append("exfiltrate_data")
        if "account_discovery" in actions:
            self.actions.append("account_discovery")
        if "lateral_movement" in actions:
            self.actions.append("lateral_movement")
        if "run_exploit" in actions:
            self.actions.append("run_exploit")
        for action in actions:
            if action not in self.actions:
                self.actions.append(action)


        self.last_action = ""

    def chose_action(self):
        last_index = self.actions.index(self.last_action)
        return self.actions

    def chose_component(self, args):
        list_of_components = args[0]

        last_index = self.actions.index(self.last_action)
        if self.last_action == "lateral_movement" and "run_exploit" in self.actions:
            last_index += 1

        return self.actions[last_index:] + self.actions[:last_index]

    def update_last_action(self, action):
        self.last_action = action



