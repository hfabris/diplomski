import network

class user_component(network.component):

    def __init__(self, id, info):

        try:
            super(user_component, self).__init__(id, info["name"], info["connected_components"])
            self.ip_address = info["ip_address"]
            self.software = info["software"]
            self.accounts = info["accounts"]
            self.domains = info["domain"]

            self.status = False
            self.active_accounts = []

        except:
            print("Invalid user component {} description".format(id))

    # Methods to get user component informations
    def get_ip_address(self): return self.ip_address

    def get_software(self): return self.software

    def get_accounts(self): return self.accounts

    def get_domains(self): return self.domains

    def get_status(self): return self.active_status
    
    def get_active_accounts(self): return self.active_accounts

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
        if self.status == True and account in self.accounts:
            del self.accounts[self.accounts.indx(account)]
            return 1
        return -1