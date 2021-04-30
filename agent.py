import strategies
import action

class agent:

    def __init__(self, name, info):
        try:
            self.name = name
            self.action_list = info["actions"]
            self.strategy = info["strategy"]
            
            # check if the strategy exists
            strategy_name = getattr(strategies, self.strategy) 
            strategy_name(self.action_list)
            
            self.knowledge = info["knowledge"]  # turn to dictionary
            self.tools = info["tools"]
            
            # check if actions exist
            # for action in self.actions:
                # action_name = getattr(actions, action)
                # action_name(self.knowledge)
            
        except:
            print("Invalid agent {} description".format(name))
            exit()


    def get_name(self):
        return self.name

    def get_actions(self):
        return self.action_list

    def get_strategy(self):
        return self.strategy

    def get_knowledge(self):
        return self.knowledge

    def get_tools(self):
        return self.tools

    def chose_action(self):
        strategy_name = getattr(strategies, self.strategy)
        return strategy_name(self.action_list)
        
    # def execute_action(self):
        # while True:
            # action = chose_action()
            # action_name = getattr(action, action)
            
            # success, results = action_name(self.knowledge)
            # if success != -1:
                # the action is executed 
                # check results and update knowledge if neccessary
                # break
    def execute_action(self, action_name, args):
        
        print("Action execution called")
        
        action_call = getattr(action, action_name)
        return action_call(self, args)





class gray_agent(agent):

    def __init__(self, info):
        super(gray_agent,self).__init__("gray_agent", info)
        self.unread_emails = []

    def add_unread_email(self,sender):
        self.unread_emails.append(sender)

    def get_unread_emails(self): 
        return self.unread_emails

    def get_oldest_unread_email(self):
        if self.unread_emails != 0:
            oldest = self.unread_emails[0]
            del self.unread_emails[0]
            return oldest
        return ""




class attacker(agent):

    def __init__(self, info):
        super(attacker,self).__init__("attacker", info)
        self.priviledge_level = {}

    def add_knowledge(self, new_knowledge):
        self.knowledge.append(new_knowledge)

    def get_priviledge_level(self, component):
        knowledge_priviledges = self.knowledge["priviledges"]
        return knowledge_priviledges.get(component, 0)

    def set_priviledge_level(self, component, priviledge_level):
        self.knowledge["priviledges"][component] = priviledge_level

    def knows_connected(component1, component2):

        connections = self.knowledge["connections"]
        if ((component1, component2) in connections) or ( (component2, component1) in connections):
            return 1
        return 0

    def knows_credentials(component):

        credentials = self.knowledge["credentials"]
        if component in credentials:
            return 1
        return 0

    def add_enumerated(component):
        self.enumerated.append(component)

    def is_enumerated(component):
        return component in self.enumerated

    def add_exfiltrated(component):
        self.exfiltrated.append(component)

    def is_exfiltrated(component):
        return component in self.exfiltrated


class defender(agent):

    def __init__(self, info):
        super(defender,self).__init__("defender", info)
        self.priviledge_level = 5

    def get_priviledge_level(self): return self.priviledge_level



