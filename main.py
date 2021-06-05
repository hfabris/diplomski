import json
import argparse

import network
import agent
import action
import graf
import random

import strategies

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

    total_footholds = []
    total_exfiltrated = []
    total_enumerated = []
    total_escalated = []

    current_time = time.time()

    for j in range(0):

        agents = {}
        for agent_name in agents_list:
            agent_call = getattr(agent, agent_name)
            agents[agent_name] = agent_call(agents_list[agent_name])

        network_list = network.network_model(system)
        network_list.add_graph(graf.make_network(network_list, possitions, height, width))

        employees = {}
        for user_component in system["user_components"]:

            user_component = system["user_components"][user_component]
            max_account_number = int(user_component["max_account_number"])
            if max_account_number > 0:
                account_number = random.randint(1, max_account_number)

                for i in range(1,account_number+1):
                    info = {}
                    info["component"] = user_component["name"]
                    info["name"] = user_component["worker_name"] + " " + str(i)
                    info["priviledge_level"] = int(user_component["priviledge_level"])
                    info["domain"] = user_component["domain"]
                    info["remote"] = user_component["remote"]
                    employee = agent.employee(info)
                    employees[employee.name] = employee


        for component in network_list.user_components:
            if component.administrators != []:
                component.add_administrator_accounts(employees)
        

        gray = agents["gray_agent"]
        attacker = agents["attacker"]
        defender = agents["defender"]

        while True:
            for employee in employees:
                employee = employees[employee]
                action_list = gray.chose_action()
                action_return = gray.execute_action(action_list, [network_list, employee, employees, agents])
                # print("\nEmployee {}".format(employee.name))

            if attacker.has_access: break

            attacker_action = attacker.chose_action()
            attacker.execute_action(attacker_action, [network_list, employee, employees, agents])

        # print(attacker.knowledge)
        # print(attacker.compromise)

        user_component_count = len(network_list.user_components)

        for i in range(user_component_count * 2):
            for employee in employees:
                employee = employees[employee]
                
                # print("\n{}".format(employee.name))
                action_list = gray.chose_action()
                action_return = gray.execute_action(action_list, [network_list, employee, employees, agents])
                if action_return == 0:
                    print("Nothing executed")
            attacker_action = attacker.chose_action()
            attacker.execute_action(attacker_action, [network_list, None, employees, agents])

            # defender_action = defender.chose_action()
            # defender.execute_action(["check_opened_connections"], [network_list, None, employees, agents])

        total_footholds.append(len(attacker.compromise["footholds"]))
        total_exfiltrated.append(len(attacker.compromise["exfiltrated"]))
        total_enumerated.append(len(attacker.compromise["enumerated"]))
        total_escalated.append(len(attacker.compromise["escalated"]))

    # print("Attacker strategy is {}".format(agents_list["attacker"]["strategy"]))
    # print("Footholds: {}".format(total_footholds))
    # print("\t mean : {} , median : {}\n".format(statistics.mean(total_footholds), statistics.median(total_footholds)))
    # print("Exfiltrated: {}".format(total_exfiltrated))
    # print("\t mean : {} , median : {}\n".format(statistics.mean(total_exfiltrated), statistics.median(total_exfiltrated)))
    # print("Enumerated: {}".format(total_enumerated))
    # print("\t mean : {} , median : {}\n".format(statistics.mean(total_enumerated), statistics.median(total_enumerated)))
    # print("Escalated: {}".format(total_escalated))
    # print("\t mean : {} , median : {}\n".format(statistics.mean(total_escalated), statistics.median(total_escalated)))

    network_list = network.network_model(system)

    for component in network_list.user_components:
        print(component.get_info())

    # component_name = "accountant_workstation"
    # component = network_list.get_component(component_name)
    # print(component)
    # print(component.name)
    # print(component.get_connected_components(network_list))
    
    
    new_time = time.time()
    diff_time = new_time - current_time
    print("Time to execute {}".format(diff_time))
    


    # network_list.add_graph(graf.make_network(network_list, possitions, height, width))
    # graf.vizualize(network_list, components_possitions)


main()
