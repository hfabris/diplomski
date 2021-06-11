import random

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
            self.account_number = 0
            self.priviledge_level = int(info["priviledge_level"])
            self.domains = info["domain"]
            self.remote = info["remote"]
            self.sensitive = info["sensitive"]
            self.user_component = True

            self.status = False
            self.active_accounts = []
            self.active_connections = {}
            self.admin_accounts = []
            self.authorized_connections = []
            self.subcomponents = []
            
            if self.max_account_number != 0:
                self.account_number = random.randint(1, self.max_account_number)
                self.subcomponents = self.make_subcomponents()

        except:
            print("Invalid user component {} description".format(id))


    def make_subcomponents(self):
        subcomponents = []

        for i in range(self.account_number):
            info = {}

            ip = list(map(int,self.ip_address.split(".")))
            ip[-1] = ip[-1]+i
            ip = ".".join(list(map(str,ip)))

            info["name"] = self.name + " " + str(i+1) 
            info["connected_components"] = [self.name]
            info["ip_address"] = ip
            info["software"] = self.software
            info["administrators"] = self.administrators
            info["max_account_number"] = 0
            info["worker_name"] = self.worker_name + " " + str(i+1)
            info["priviledge_level"] = self.priviledge_level
            info["domain"] = self.domains
            info["remote"] = self.remote
            info["sensitive"] = self.sensitive

            comp = user_component(info["name"], info)
            subcomponents.append(comp)

        return subcomponents


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

    def remove_all_active_accounts(self, employees):
        if self.status == True:
            for account in self.active_accounts:
                empl = employees[account]
                empl.remove_login(self.name)
            self.active_accounts = []
            return 1
        return -1

    # Methods to add, remove and get connections between this component and other components
    def add_active_connection(self, other_component, agent):
        if self.status == True or "attacker" in agent:
            self.active_connections[other_component] = self.active_connections.setdefault(other_component, [])
            if agent not in self.active_connections[other_component]:
                self.active_connections[other_component].append(agent)
            # self.active_connections.append( (other_component, agent) )
            return 1
        return -1
    
    def remove_all_active_connections(self, network, employees):
        for connection in self.active_connections:
            other_component = network.get_component(connection)
            for accounts in self.active_connections[connection]:
                employee1, employee2 = accounts

                other_component.remove_active_connection(self, employee1, employee2)

                employee1 = employees[employee1]
                employee2 = employees[employee2]

                employee1.remove_connection(employee2.name)
                employee2.remove_connection(employee1.name)

        self.active_connections = {}


    def remove_active_connection(self, other_component, employee1, employee2):

        
        active_connections = self.active_connections[other_component.name]
        
        if (employee1, employee2) in active_connections:
            del active_connections[active_connections.index((employee1, employee2))]
        
        elif (employee2, employee1) in active_connections:
            del active_connections[active_connections.index((employee2, employee1))]
        
        else:
            return 0
        
        if active_connections == []:
            del self.active_connections[other_component.name]
        else:
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

    def set_connected_components(self, network):

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

                for component in current_comp.connected_components:
                    if component not in visited and component not in to_visit:
                        to_visit.add(component)

        new_connected = []
        for component in connected:
            component = network.get_component(component)
            if component.subcomponents != []:
                for subcomponent in component.subcomponents:
                    if subcomponent.name != self.name:
                        new_connected.append(subcomponent.name)
            else:
                new_connected.append(component.name)
        
        self.authorized_connections = new_connected

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
        connected = "\n\t".join(x for x in self.connected_components)
        sensitive = "\n\t".join(x for x in self.sensitive)
        softwares = "\n\t" + "\n\t".join(x for x in self.software)
        
        active_accounts = "\n\t"
        active_connections = "\n\t"
        if self.subcomponents != []:
            for subcomponent in self.subcomponents:
                active = "\n\t".join(subcomponent.active_accounts)
                if active != "":
                    active_accounts = active_accounts + active + "\n\t"
                
                admins = "\n\t" + "\n\t".join(x for x in subcomponent.admin_accounts)

                for connected_component in subcomponent.active_connections:
                    for connection in subcomponent.active_connections[connected_component]:
                        if "attacker" in connection: continue
                        comp_x, comp_y = connection
                        if comp_x == subcomponent.worker_name:
                            active_connections += comp_x + " <-> " + comp_y + "\n\t"
                        else:
                            active_connections += comp_y + " <-> " + comp_x + "\n\t"
        else:
            admins = "\n\t" + "\n\t".join(x for x in self.admin_accounts)
            active_accounts = "\n\t" + "\n\t".join(x for x in self.active_accounts)
            active_connections = "\n\t" + "\n\t".join(x for x in self.active_connections)
        
        info = '''
Component name : {}
Connected components: {}
Component ip address: {}
Component administrators : {}
Sensitive informations on component : {}
Installed software on component: {}
Active accounts:  {}
Active connections : {}
        '''.format(self.name, connected, self.ip_address, admins, sensitive, softwares, active_accounts, active_connections)

        return info

    def reset_component(self):
        self.status = False
        self.active_accounts = []
        self.active_connections = {}

# class to make network model from components descriptions
# network model consists of user and network components
class network_model:

    def __init__(self, components):

        self.user_components = []
        self.network_components = []
        self.subcomponents = []
        try:
            for c in components["user_components"]:
                self.user_components.append(user_component(c,components["user_components"][c]))
            for c in components["network_components"]:
                self.network_components.append(network_component(c,components["network_components"][c]))
                
            for component in self.user_components:
                if component.subcomponents != []:
                    self.subcomponents += component.subcomponents
        except:
            print("Invalid network description")
            exit()

        self.components_list = self.user_components + self.network_components + self.subcomponents
        self.components_names = set( component.name for component in self.components_list )

        for u_component in self.subcomponents:
            u_component.set_connected_components(self)


    def get_accessible_components(self):
        accessible = []
        for component in self.user_components:
            if component.subcomponents == []:
                accessible.append(component)
        accessible += self.subcomponents
        
        return accessible

    def get_number_of_components(self):

        number_of_components = 0

        for component in self.user_components:
            if component.subcomponents == []:
                number_of_components += 1
            else:
                number_of_components += len(component.subcomponents)

        return number_of_components

    def get_components(self):
        return self.network_components + self.user_components

    def get_component(self, component_name):
        for component in self.components_list:
            if component.name == component_name:
                return component
        return -1

    def add_graph(self, graph): 
        self.graph = graph

    def reset_all_components(self):
        for component in self.subcomponents:
            component.reset_component()
        for component in self.user_components:
            component.reset_component()