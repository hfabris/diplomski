
class action:
    
    def __init__(self, name, info):
        try:
            self.name = name
            self.preconditions = info["preconditions"]
            self.postconditions = info["postconditions"]
            self.success = info["success probability"]
            # strategy_name = getattr(strategies, self.strategy) 
            # strategy_name(self.actions)
        except:
            print("Invalid action {} description".format(name))

    def get_preconditions(): return self.preconditions
    
    def get_postconditions(): return self.postconditions
    
    def get_success_probability(): return self.success


# action reboot host
# if the agent has access to a host the action is executed
# probability of success is 1 and the credentials are flushed
# if the preconditions are not satisfied, return -1
def reboot_host(knowledge):
    if "has_access" in knowledge:
        return 1, "flush_credentials"
    return -1, ""

# action user login to a host
# if the preconditions are satisfied, credentials are stored, probability of success is 1
# if the preconditions are not satisfied, return -1
def user_login_to_host(knowledge):
    if True: # write preconditions 
        return 1, "store_credentials"
    return -1, ""
