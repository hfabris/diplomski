class component:
    
    def __init__(self, id, info):
        try:
            self.id = id
            self.name = info["name"]
            self.connected_components = info["connected_components"]
            if len(info) > 2:
                self.ip_address = info["ip_address"]
                self.software = info["software"]
                self.accounts = info["accounts"]
                self.domain = info["domain"]
                self.network_component = False
            else:
                self.network_component = True
        except:
            print("Invalid component {} description".format(id))

    def get_id(self): return self.id
    
    def get_name(self): return self.name
    
    def get_connected_components(self): return self.connected_components
    
    


class network_model:

    def __init__(self, components):
        
        self.user_components = []
        self.network_components = []
        try:
            for c in components["user_components"]:
                self.user_components.append(component(c,components["user_components"][c]))
            for c in components["network_components"]:
                self.network_components.append(component(c,components["network_components"][c]))
        except:
            print("Invalid network description")
            exit()
 
        self.components_list = self.user_components + self.network_components
        self.components_names = set( component.name for component in self.components_list )
        
        # print(self.components_names)
        
        # self.network = self.connect_components(self.components_list, self.components_names)
 

    def get_user_components(self):
        return self.user_components

    def get_network_components(self):
        return self.network_components

    def connect_components(self, components, names):
        # print(components)
        for component in components:
            print(component.get_connected_components())


    def get_user_components(self):
        return self.user_components

    def get_network_components(self):
        return self.network_components

    def get_components(self):
        return self.network_components + self.user_components

    # def connect(self,user_components, network_components):
        
        # user = user_components[:]
        # network = network_components[:]
        
        # network = {}
        # layer = 0
        # network_layers = {}
        
        # nodes = set()
        
        
        # while network != []:
            
            # new_network = network[:]
            # new_users = []
            # visited = []
            # layer += 1
            
            # for component in user:
                # if component not in visited: 
                
                    # visited.append(component)
                    
                    # no upper layer
                    # if network == []:
                        
                    # else:
                    
                    # connected_components = component.get_connected_components()
                    
                    # same_layer = [component]
                    # next_layer_component = ""
                    # for new_component in connected_components:
                        # if new_component in network:
                            # next_layer_component = new_component
                            # break
                        # else:
                            # same_layer.append(new_component)
                            # visited.append(new_component)
                    
                    # del new_network[new_network.index(next_layer_component)]
                    # new_users.append(next_layer_component)
                
                    # upper_layer_component = next_layer_component.get_connected_components() 
                    # lower_layer = []
                    
                    # for new_component in upper_layer_component:
                        # if new_component in new_users:
                            # del new_users[new_users.index(new_component)]
                            # visited.append(new_component)
                            # lower_layer.append(new_component)
            
            # network = new_network
            # user = new_users





