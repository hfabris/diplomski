import random

# class for random strategy
# employees and defender will always have random strategy
# class has methods for chosing actions, chosing components
class Random():

    def __init__(self, actions):
        self.actions = actions
        self.last_action = ""

    def chose_action(self):
        random.shuffle(self.actions)
        return self.actions

    def chose_component(self, args):
        list_of_components = args[0]
        return random.choice(list_of_components)

    def update_last_action(self, action):
        self.last_action = action


# class Greedy():

    # def __init__(actions, network):
        # self.actions = actions
        # self.network = network
        # self.last_action = ""

    # def chose_action(self):
        







