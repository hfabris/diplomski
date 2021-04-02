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
 

    def get_user_components(self):
        return self.user_components

    def get_network_components(self):
        return self.network_components






