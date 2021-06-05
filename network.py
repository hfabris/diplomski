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


class network_component(component):
    
    def __init__(self, id, info):
        try:
            super(network_component, self).__init__(id, info["name"], info["connected_components"])
            self.user_component = False
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
            self.administrators = info["administrators"]
            self.max_account_number = int(info["max_account_number"])
            self.worker_name = info["worker_name"]
            self.priviledge_level = info["priviledge_level"]
            self.domains = info["domain"]
            self.remote = info["remote"]
            self.sensitive = info["sensitive"]
            self.user_component = True

            self.status = False
            self.active_accounts = []
            self.active_connections = {}
            self.admin_accounts = []

        except:
            print("Invalid user component {} description".format(id))


    # Method to put status of component
    # If the status is True, the component is active and the user is logged in
    def set_status(self, status): self.status = status 

    # Methods to add or remove account to/from the list of active account on this component
    # Component needs to be active to be able to add or remove accounts
    # if the method is successful it returns 1, otherwise it returns -1
    def add_active_account(self, account_name):
        if self.status == True:
            self.active_accounts.append(account_name)
            return 1
        return -1

    def remove_active_account(self,account):
        if self.status == True and account in self.active_accounts:
            del self.active_accounts[self.active_accounts.index(account)]
            return 1
        return -1

    def remove_all_active_accounts(self):
        if self.status == True:
            self.active_accounts = []
            return 1
        return -1

    # Methods to add, remove and get connections between this component and other components
    def add_active_connection(self, other_component, agent):
        if self.status == True:
            self.active_connections[other_component] = self.active_connections.setdefault(other_component, [])
            self.active_connections[other_component].append(agent)
            # self.active_connections.append( (other_component, agent) )
            return 1
        return -1
    
    def remove_active_connection(self, other_component, employee1, employee2):
        
        active_connections = self.active_connections[other_component.name]
        
        if (employee1, employee2) in active_connections:
            del active_connections[active_connections.index((employee1, employee2))]
        
        elif (employee2, employee1) in active_connections:
            del active_connections[active_connections.index((employee2, employee1))]
        
        else:
            return 0
        
        self.active_connections[other_component.name] = active_connections
        return 1

    def remove_attacker_connection(self, other_component):
        active_connections = self.active_connections.get(other_component.name, "")
        if active_connections != "":
            self.active_connections[other_component.name] = []

    def is_vulnerable(self, exploit):
        if exploit in self.vulnerable:
            return 1
        return 0

    def get_connected_components(self, network):
        to_visit = set(self.connected_components)
        visited = set()
        connected = set()

        while to_visit:
            current_comp = network.get_component(to_visit.pop())
            if current_comp.name not in visited: 
                visited.add(current_comp.name)
                if current_comp.user_component == True and current_comp.name != self.name:
                    if current_comp.name in self.remote:
                        connected.add(current_comp.name)
                    else:    
                        for domain in current_comp.domains:
                            if domain in self.domains:
                                connected.add(current_comp.name)
                            # print("\n")
                            # print(current_comp.name)
                            # print(current_comp.domains, self.domains)

                for component in current_comp.connected_components:
                    if component not in visited and component not in to_visit:
                        to_visit.add(component)

        return connected

    def add_administrator_accounts(self, employees):
        for employee in employees:
            employee_name = employee.split(" ")
            if employee_name[-1].isdigit():
                employee_name = " ".join(employee_name[:-1])
            else:
                employee_name = " ".join(employee_name)
            if employee_name in self.administrators:
                self.admin_accounts.append(employee)

    def get_info(self):
        # print(self.name)
        # print(self.connected_components)
        # print(self.admin_accounts)
        # print(self.sensitive)
        # print(self.software)
        # print(self.active_accounts)
        # print(self.active_connections)
        connected = ", ".join(x for x in self.connected_components)
        admins = ", ".join(x for x in self.admin_accounts)
        sensitive = ", ".join(x for x in self.sensitive)
        softwares = ", ".join(x for x in self.software)
        active_accounts = ", ".join(x for x in self.active_accounts)
        active_connections = ", ".join(x for x in self.active_connections)
        info = '''
Component name : {}
Connected components: {}
Component ip address: {}
Component administrators : {}
Sensitive informations on component : {}
Installed software on component: {}
Active accounts: {}
Active connections : {}
        '''.format(self.name, connected, self.ip_address, admins, sensitive, softwares, active_accounts, active_connections)
        
        
        return info

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


    def get_components(self):
        return self.network_components + self.user_components

    def get_component(self, component_name):
        for component in self.components_list:
            if component.name == component_name:
                return component
        return -1

    def add_graph(self, graph): 
        self.graph = graph
