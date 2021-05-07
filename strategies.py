import random

# class for random strategy
# employees and defender will always have random strategy
# class has methods for chosing actions, chosing components
class Random():

    def __init__(self, actions, network):
        self.actions = actions
        self.network = network
        self.last_action = ""

    def chose_action(self):
        random.shuffle(self.actions)
        return self.actions

    def chose_component(self, agent):
        while True:
            user_components = self.network.get_user_components()
            chosen_component = user_components[random.randint(0,len(user_components)-1)].get_name()
            if chosen_component != agent.component_name:
                return chose_component

    def update_last_action(self, action):
        self.last_action = action


# class Greedy():

    # def __init__(actions, network):
        # self.actions = actions
        # self.network = network
        # self.last_action = ""

    # def chose_action(self):
        







