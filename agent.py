import strategies
import action

class agent:

    def __init__(self, name, info):
        try:
            self.name = name
            self.action_list = info["actions"]
            self.strategy = info["strategy"]
            
            # check if the strategy exists
            strategy_name = getattr(strategies, self.strategy) 
            strategy_name(self.action_list)
            
            self.knowledge = info["knowledge"]
            self.tools = info["tools"]
            
            # check if actions exist
            # for action in self.actions:
                # action_name = getattr(actions, action)
                # action_name(self.knowledge)
            
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

    def chose_action(self):
        strategy_name = getattr(strategies, self.strategy)
        return strategy_name(self.action_list)
        
    def execute_action(self):
        while True:
            action = chose_action()
            action_name = getattr(action, action)
            
            success, results = action_name(self.knowledge)
            if success != -1:
                # the action is executed 
                # check results and update knowledge if neccessary
                break
                






