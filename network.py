# class to describe general informations about components
# every component has id, name, and connected_components
class component:

    def __init__(self, id, name, connected):
        try:
            self.id = id
            self.name = name
            self.connected_components = connected
            
        except:
            print("Invalid component {} description".format(id))

    def get_id(self): return self.id

    def get_name(self): return self.name

    def get_connected_components(self): return self.connected_components


class network_component(component):
    
    def __init__(self, id, info):
        try:
            super(network_component, self).__init__(id, info["name"], info["connected_components"])
        except:
            print("Invalid network component {} description".format(id))


# class which describes user component
# additional informations which user components have include ip address, software, max number of accounts, priviledge level and domain
class user_component(component):

    def __init__(self, id, info):

        try:
            super(user_component, self).__init__(id, info["name"], info["connected_components"])
            self.ip_address = info["ip_address"]
            self.software = info["software"]
            self.accounts = info["accounts"]
            self.max_account_number = info["max_account_number"]
            self.priviledge_level = info["priviledge_level"]
            self.domains = info["domain"]

            self.status = False
            self.active_accounts = []
            self.active_connections = []

        except:
            print("Invalid user component {} description".format(id))

    # Methods to get user component informations
    def get_ip_address(self): return self.ip_address

    def get_software(self): return self.software

    def get_accounts(self): return self.accounts

    def get_domains(self): return self.domains

    def get_status(self): return self.status
    
    def get_active_accounts(self): return self.active_accounts
    
    def is_account_active(self, account):
        if account in self.active_accounts: return True
        return False

    # Method to put status of component
    # If the status is True, the component is active and the user is logged in
    def set_status(self, status): self.status = status 

    # Methods to add or remove account to/from the list of active account on this component
    # Component needs to be active to be able to add or remove accounts
    # if the method is successful it returns 1, otherwise it returns -1
    def add_active_account(self, account):
        if self.status == True:
            self.active_accounts.append(account)
            return 1
        return -1

    def remove_active_account(self,account):
        if self.status == True and account in self.active_accounts:
            del self.active_accounts[self.active_accounts.index(account)]
            return 1
        return -1

    # Methods to add, remove and get connections between this component and other components
    def add_active_connection(self, other_component, agent):
        if self.status == True:
            self.active_connections.append( (other_component, agent) )
            return 1
        return -1
    
    def remove_active_connection(self, other_component, agent):
        
        if (other_component, agent) in self.active_connections:
            del self.active_connections[self.active_connections.index( (other_component, agent) )]
            return 1
        return -1
    
    def get_active_connections(self): return self.active_connections

# class to make network model from components descriptions
# network model consists of user and network components
class network_model:

    def __init__(self, components):

        self.user_components = []
        self.network_components = []
        try:
            for c in components["user_components"]:
                self.user_components.append(user_component(c,components["user_components"][c]))
            for c in components["network_components"]:
                self.network_components.append(network_component(c,components["network_components"][c]))
        except:
            print("Invalid network description")
            exit()

        self.components_list = self.user_components + self.network_components
        self.components_names = set( component.name for component in self.components_list )


    def get_user_components(self):
        return self.user_components

    def get_network_components(self):
        return self.network_components

    def get_components(self):
        return self.network_components + self.user_components

    def get_component(self, component_name):
        for component in self.components_list:
            if component.get_name() == component_name:
                return component
        return -1

    def add_graph(self, graph): 
        self.graph = graph

    def get_graph(self): 
        return self.graph