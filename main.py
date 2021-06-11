import json
import argparse

import network
import agent
import action
import graf
import random

import strategies
import copy

import time
import statistics

# python main.py --agents agent.txt --system model_sustava.txt --components component_possitions.txt
def main():

    # Add parser to parse input arguments
    # Neccessary argument to start a program are files with agents, system and actions descriptions
    parser = argparse.ArgumentParser(description='Emulation of Automated Attackers in Cybersecurity')
    parser.add_argument('--system', metavar='system', nargs=1, help='an imput file with system descriptions', required=True)
    parser.add_argument('--agents', metavar='agents', nargs=1, help='an input file with agents descriptions', required=True)
    parser.add_argument('--components', metavar='agents', nargs=1, help='an input file with components possitions', required=True)

    args = parser.parse_args()

    # Read input arguments and parse json files
    with open(args.agents[0]) as agents_file:
        agents_list = json.loads(agents_file.read())
    with open(args.system[0]) as system_file:
        system = json.loads(system_file.read())
    with open(args.components[0]) as system_file:
        components_possitions = json.loads(system_file.read())

    height = int(components_possitions["dimensions"]["height"])
    width = int(components_possitions["dimensions"]["width"])
    possitions = components_possitions["components"]

    current_time = time.time()

    attacker_statistics = {}
    attacker_progress = {}
    for strategy in agents_list["attacker"]["strategy"]:
        attacker_statistics[strategy] = {}
        attacker_statistics[strategy]["total_footholds"] = []
        attacker_statistics[strategy]["total_exfiltrated"] = []
        attacker_statistics[strategy]["total_enumerated"] = []
        attacker_statistics[strategy]["total_escalated"] = []

        attacker_progress[strategy] = {}

    number_of_rounds = []

    for j in range(50):
        
        pre_game = []

        agents = {}
        for agent_name in agents_list:
            agent_call = getattr(agent, agent_name)
            agents[agent_name] = agent_call(agents_list[agent_name])

        network_list = network.network_model(system)
        network_list.add_graph(graf.make_network(network_list, possitions, height, width))

        employees = {}
        for user_component in network_list.user_components:

            account_number = user_component.account_number
            if account_number > 0:

                for i in range(1,account_number+1):
                    info = {}
                    info["component"] = user_component.name + " " + str(i)
                    info["name"] = user_component.worker_name + " " + str(i)
                    info["priviledge_level"] = user_component.priviledge_level
                    info["domain"] = user_component.domains
                    info["remote"] = user_component.remote
                    employee = agent.employee(info)
                    employees[employee.name] = employee


        for component in network_list.user_components:
            if component.administrators != []:
                if component.subcomponents != []:
                    for subcomponent in component.subcomponents:
                        subcomponent.add_administrator_accounts(employees)
                else:
                    component.add_administrator_accounts(employees)
        
        gray = agents["gray_agent"]
        attacker = agents["attacker"]
        defender = agents["defender"]

        while True:
            for employee in employees:
                employee = employees[employee]
                action_list = gray.chose_action()
                exectuted_action = ""
                other = ""
                while True:
                    action = action_list[0]
                    del action_list[0]
                    action_return = gray.execute_action(action, [network_list, employee, employees, agents])
                    if type(action_return) != int:
                        other = action_return[1]
                        action_return = action_return[0]
                        # print(action, other)
                    if action_return == 1:
                        exectuted_action = action
                        break
                    elif action_return == -1:
                        print("\nProblem while executing action {}\n".format(action))
                        break
                    if action_list == []:
                        print("\nAll actions tested, none executed\n")
                        break
                if exectuted_action != "" :
                    pre_game.append( (employee.name, exectuted_action, other) )

            if attacker.has_access: break
            exectuted_action = ""
            attacker_action = attacker.chose_action()
            while True:
                action = attacker_action[0]
                del attacker_action[0]
                action_return = attacker.execute_action(action, [network_list, None, employees, agents])
                if type(action_return) != int:
                    other = action_return[1]
                    action_return = action_return[0]
                if action_return == 1:
                    exectuted_action = action
                    break
                elif action_return == -1:
                    print("\nProblem while executing action {}\n".format(action))
                    break
                if attacker_action == []:
                    print("\nAll actions tested, none executed\n")
                    break
            if exectuted_action != "":
                pre_game.append( ("attacker", exectuted_action, other) )

        user_component_count = network_list.get_number_of_components()
        number_of_rounds.append(user_component_count * 2)
        # print("Round {} has {} components".format(j, user_component_count))

        emulation_data = {}
        
        for i in range(user_component_count * 2):
            round_actions = []
            for employee in employees:
                employee = employees[employee]
                
                action_list = gray.chose_action()
                exectuted_action = ""
                while True:
                    action = action_list[0]
                    del action_list[0]
                    action_return = gray.execute_action(action, [network_list, employee, employees, agents])
                    if type(action_return) != int:
                        other = action_return[1]
                        action_return = action_return[0]
                    if action_return == 1:
                        exectuted_action = action
                        break
                    elif action_return == -1:
                        print("\nProblem while executing action {}\n".format(action))
                        break
                    if action_list == []:
                        print("\nAll actions tested, none executed\n")
                        break
            
                if exectuted_action != "" :
                    round_actions.append( (employee.name, exectuted_action, other) )

            exectuted_action = ""
            defender_action = defender.chose_action()
            while True:
                action = defender_action[0]
                del defender_action[0]
                action_return = defender.execute_action(action, [network_list, None, employees, agents])
                if type(action_return) != int:
                    other = action_return[1]
                    action_return = action_return[0]
                if action_return == 1:
                    exectuted_action = action
                    break
                elif action_return == -1:
                    print("\nProblem while executing action {}\n".format(action))
                    break
                if defender_action == []:
                    print("\nAll actions tested, none executed\n")
                    break
                
            if exectuted_action != "" :
                round_actions.append( ("defender", exectuted_action, other) )

            emulation_data[i] = round_actions

        # Emulate the game
        for attacker_strategy in attacker.strategies:
            attacker.set_strategy(attacker_strategy)
            
            network_list.reset_all_components()
            
            for employee in employees:
                employees[employee].reset_employee
            
            attacker.reset()
            
            for action in pre_game:
                employee, action, optional = action
                if employee != "attacker":
                    employee = employees[employee]
                    action_return = gray.execute_action(action, [network_list, employee, employees, agents], optional)
                else:
                    action_return = attacker.execute_action(action, [network_list, None, employees, agents], optional)

            
            attacker_progress[attacker_strategy][j] = {}
            attacker_progress[attacker_strategy][j][0] = {}
            attacker_progress[attacker_strategy][j][0]["action"] = ("", "")
            attacker_progress[attacker_strategy][j][0]["knowledge"] = copy.deepcopy(attacker.knowledge)
            attacker_progress[attacker_strategy][j][0]["compromise"] = copy.deepcopy(attacker.compromise)

            for i in range(user_component_count * 2 ):
                attacker_progress[attacker_strategy][j][i+1] = {}
                attacker_progress[attacker_strategy][j][i+1]["action"] = {}
                attacker_progress[attacker_strategy][j][i+1]["knowledge"] = {}
                attacker_progress[attacker_strategy][j][i+1]["compromise"] = {}

                round_actions = emulation_data[i]
                defender_action = round_actions[-1]
                del round_actions[-1]
                
                for employee, action, optional in round_actions:
                    employee = employees[employee]
                    action_return = gray.execute_action(action, [network_list, employee, employees, agents], optional)
                    
                attacker_action = attacker.chose_action()
                while True:
                    action = attacker_action[0]
                    del attacker_action[0]
                    action_return = attacker.execute_action(action, [network_list, None, employees, agents])
                    if type(action_return) != int:
                        other = action_return[1]
                        action_return = action_return[0]
                    if action_return == 1:
                        exectuted_action = action
                        attacker_progress[attacker_strategy][j][i+1]["action"] = ( action, other )
                        # print("Attacker with strategy {} executed action {} in round {}\n".format(attacker_strategy, action, i))
                        attacker.strategy.update_last_action(action)
                        break
                

                action_return = defender.execute_action(defender_action[1], [network_list, None, employees, agents], defender_action[2])
                
                # Save attacker knowledge and compromise for analysis
                attacker_progress[attacker_strategy][j][i+1]["knowledge"] = copy.deepcopy(attacker.knowledge)
                attacker_progress[attacker_strategy][j][i+1]["compromise"] = copy.deepcopy(attacker.compromise)

            attacker_statistics[attacker_strategy]["total_footholds"].append(len(attacker.compromise["footholds"]))
            attacker_statistics[attacker_strategy]["total_exfiltrated"].append(len(attacker.compromise["exfiltrated"]))
            attacker_statistics[attacker_strategy]["total_enumerated"].append(len(attacker.compromise["enumerated"]))
            attacker_statistics[attacker_strategy]["total_escalated"].append(len(attacker.compromise["escalated"]))


    

    print("Total number of rounds:")
    print(number_of_rounds)

    for strategy in attacker_statistics:
        
        
        total_footholds = attacker_statistics[strategy]["total_footholds"]
        total_footholds_percent = [(x/y)*100 for x,y in zip(total_footholds, number_of_rounds)]

        total_exfiltrated = attacker_statistics[strategy]["total_exfiltrated"]
        total_exfiltrated_percent = [(x/y)*100 for x,y in zip(total_exfiltrated, number_of_rounds)]

        total_enumerated = attacker_statistics[strategy]["total_enumerated"]
        total_enumerated_percent = [(x/y)*100 for x,y in zip(total_enumerated, number_of_rounds)]

        total_escalated = attacker_statistics[strategy]["total_escalated"]
        total_escalated_percent = [(x/y)*100 for x,y in zip(total_escalated, number_of_rounds)]
        
        print("\n")
        print("Attacker strategy is {}".format(strategy))
        print("Footholds: {}".format(total_footholds))
        print("\t max : {:.02f} % , min : {:.02f} % , mean : {:0.2f} % , median : {:0.2f} %\n".format(max(total_footholds_percent), min(total_footholds_percent), statistics.mean(total_footholds_percent), statistics.median(total_footholds_percent)))

        print("Exfiltrated: {}".format(total_exfiltrated))
        print("\t max : {:.02f} % , min : {:.02f} % , mean : {:0.2f} % , median : {:0.2f} %\n".format(max(total_exfiltrated_percent), min(total_exfiltrated_percent), statistics.mean(total_exfiltrated_percent), statistics.median(total_exfiltrated_percent)))

        print("Enumerated: {}".format(total_enumerated))
        print("\t max : {:.02f} % , min : {:.02f} % , mean : {:0.2f} % , median : {:0.2f} %\n".format(max(total_enumerated_percent), min(total_enumerated_percent), statistics.mean(total_enumerated_percent), statistics.median(total_enumerated_percent)))

        print("Escalated: {}".format(total_escalated))
        print("\t max : {:.02f} % , min : {:.02f} % , mean : {:0.2f} % , median : {:0.2f} %\n".format(max(total_escalated_percent), min(total_escalated_percent), statistics.mean(total_escalated_percent), statistics.median(total_escalated_percent)))

    
    
    new_time = time.time()
    diff_time = new_time - current_time
    print("Time to execute {}".format(diff_time))

    network_list.add_graph(graf.make_network(network_list, possitions, height, width))
    graf.vizualize(network_list, components_possitions, attacker_progress)


main()
