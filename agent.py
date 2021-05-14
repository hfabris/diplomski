import strategies
import action
import random

class agent:

    def __init__(self, name, info):
        try:
            self.name = name
            self.action_list = info["actions"]
            
            self.strategy = getattr(strategies, info["strategy"])
            self.strategy = self.strategy(self.action_list)
            
            self.knowledge = info["knowledge"]  # turn to dictionary
            self.tools = info["tools"]

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

    def chose_action(self, network):
        return self.strategy.chose_action()

    def execute_action(self, action_names, args):

        for action_name in action_names:
            
            action_call = getattr(action, action_name)
            action_return = action_call(self,args)
            if action_return == 1:
                self.strategy.update_last_action(action_name)
                print("Executed action {}".format(action_name))
                return 1
                
        return 0



class employee():

    def __init__(self, info):
        self.component = info["component"]
        self.name = info["name"]
        self.priviledge_level = info["priviledge_level"] 
        self.domain = info["domain"]
        self.active_connections = []
        self.unread_emails = []

    def get_component(self):
        return self.component

    def get_name(self):
        return self.name

    def get_priviledge_level(self):
        return self.priviledge_level

    def get_domain(self):
        return self.domain

    def get_active_connections(self):
        return self.active_connections

    def add_connections(self, connection):
        self.active_connections.append(connection.get_name())

    def remove_connection(self, employee):
    
        if employee in self.active_connections:
            del self.active_connections[self.active_connections.index(employee)]
            return 1
        return 0

    def add_unread_email(self,sender):
        self.unread_emails.append(sender)

    def get_unread_emails(self): 
        return self.unread_emails

    def get_random_email(self):
        if self.unread_emails != 0:
            random_email = random.choice(self.unread_emails)
            return random_email
        return ""

    def get_oldest_unread_email(self):
        if self.unread_emails != 0:
            oldest = self.unread_emails[0]
            del self.unread_emails[0]
            return oldest
        return ""


class gray_agent(agent):

    def __init__(self, info):
        super(gray_agent,self).__init__("gray_agent", info)





class attacker(agent):

    def __init__(self, info):
        super(attacker,self).__init__("attacker", info)
        self.priviledge_level = {}
        self.compromise = {}
        
        self.knowledge["credentials"] = []              # list of credentials attacker has found in system
        self.knowledge["connected"] = []                # list of tuples, (component_X, component_Y), where component_X and component_Y are connected
        self.knowledge["local_admins"] = []             # list of tuples, (component, local admins of component)
        self.knowledge["active_connections"] = []       # list of active connections attacker knows
        self.knowledge["remote"] = []                   # list of tuples, (account_A, component_X), where account_A is authorized to remotely log in to component_X 
        
        self.compromise["footholds"] = []               # list of components attacker has established foothold on 
        self.compromise["probed_host"] = []             # list of hosts attacker has probed to find admins
        self.compromise["exfiltrated"] = []             # list of components attacker has exfiltrated data from
        self.compromise["enumerated"] = []              # list of components attacker has enumerated 
        self.compromise["escalated"] = []               # list of components attacker has escalated footholds on
        self.compromise["exploited"] = []               # list of tuples, (host_X, exploit_E), where attacker has tried to exploit host_X with exploit_E
        
        self.current_component = None

    def add_knowledge(self, category, new_knowledge):
        self.knowledge[category].append(new_knowledge)

    def add_compromise(self, category, new_compromise):
        self.compromise[category].append(new_compromise)

    def get_priviledge_level(self, component):
        knowledge_priviledges = self.knowledge["priviledges"]
        return knowledge_priviledges.get(component, 0)

    def set_priviledge_level(self, component, priviledge_level):
        self.knowledge["priviledges"][component] = priviledge_level

    def knows_connected(component1, component2):

        connections = self.knowledge["connected"]
        if ((component1, component2) in connections) or ( (component2, component1) in connections):
            return 1
        return 0

    def knows_credentials(self,component):

        credentials = self.knowledge["credentials"]
        if component in credentials:
            return 1
        return 0

    def is_enumerated(self, component):
        return component in self.compromise["enumerated"]

    def is_exfiltrated(self, component):
        return component in self.compromise["exfiltrated"]

    def get_current_component(self):
        return self.current_component

    def set_current_component(self, component):
        self.current_component = component

    def add_foothold(self, component):
        self.compromise["footholds"].append(component)

class defender(agent):

    def __init__(self, info):
        super(defender,self).__init__("defender", info)
        self.priviledge_level = 5

    def get_priviledge_level(self): return self.priviledge_level



