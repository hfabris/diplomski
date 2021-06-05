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

    def chose_action(self):
        return self.strategy.chose_action()

    def execute_action(self, action_names, args):

        for action_name in action_names:

            action_call = getattr(action, action_name)
            action_return = action_call(self,args)
            if action_return == 1:
                self.strategy.update_last_action(action_name)
                # if self.name == "gray_agent":
                    # print("Employee {} executed action {}".format(args[1].name, action_name))
                # print("Executed action {}\n".format(action_name))
                return 1
            elif action_return == -1:
                print("\n\n\nFailed to execute action {}\n\n\n".format(action_name))
                
        return 0



class employee():

    def __init__(self, info):
        self.component = info["component"]
        self.name = info["name"]
        self.priviledge_level = info["priviledge_level"] 
        self.domain = info["domain"]
        self.remote = info["remote"]

        self.active_connections = []
        self.unread_emails = []
        self.active_logins = []

    def get_priviledge_level(self):
        return self.priviledge_level

    def add_connections(self, connection):
        self.active_connections.append(connection.name)


    def remove_connection(self, employee):
    
        if employee in self.active_connections:
            del self.active_connections[self.active_connections.index(employee)]
            return 1
        return 0

    def add_login(self, component):
        self.active_logins.append(component)

    def remove_login(self, component):
        if component in self.active_logins:
            del self.active_logins[self.active_logins.index(component)]
            return 1
        return 0

    def add_unread_email(self,sender):
        self.unread_emails.append(sender)

    def get_random_email(self):
        if self.unread_emails != []:
            random_email = random.choice(self.unread_emails)
            del self.unread_emails[self.unread_emails.index(random_email)]
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
        self.has_access = False
        
        self.knowledge["credentials"] = []              # list of credentials attacker has found in system
        self.knowledge["connected"] = []                # list of tuples, (component_X, component_Y), where component_X and component_Y are connected
        self.knowledge["local_admins"] = []             # list of tuples, (component, local admins of component)
        self.knowledge["active_connections"] = []       # list of active connections attacker knows
        self.knowledge["remote"] = []                   # list of tuples, (account_A, component_X), where account_A is authorized to remotely log in to component_X 
        
        self.compromise["footholds"] = []               # list of components attacker has established foothold on 
        self.compromise["probed_accounts"] = []         # list of hosts attacker has probed to find admins
        self.compromise["exfiltrated"] = []             # list of components attacker has exfiltrated data from
        self.compromise["enumerated"] = []              # list of components attacker has enumerated 
        self.compromise["escalated"] = []               # list of components attacker has escalated footholds on
        self.compromise["exploited"] = []               # list of components attacker has tried to exploit with exploits in his toolbox

        # self.current_component = None

    def add_knowledge(self, category, new_knowledge):
        if new_knowledge not in self.knowledge[category]:
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

    # def set_current_component(self, component):
        # self.current_component = component

    def add_foothold(self, component):
        self.has_access = True
        self.compromise["footholds"].append(component)

    def del_foothold(self, footholds):
        for foothold in footholds:
            if foothold in self.compromise["footholds"]:
                foothold_index = self.compromise["footholds"].index(foothold)
                del self.compromise["footholds"][foothold_index]
            if foothold in self.compromise["escalated"]:
                escalated_index = self.compromise["escalated"].index(foothold)
                del self.compromise["escalated"][escalated_index]
        if len(self.compromise["footholds"]) == 0:
            self.has_access == False



class defender(agent):

    def __init__(self, info):
        super(defender,self).__init__("defender", info)
        self.priviledge_level = 5



