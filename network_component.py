import network

class network_component(network.component):
    
    def __init__(self, id, info):
        try:
            super(network_component, self).__init__(id, info["name"], info["connected_components"])
        except:
            print("Invalid network component {} description".format(id))