import json
import argparse

import network
import agent
import action
import graf

# python main.py --agents agent.txt --actions actions.txt --system model_sustava.txt
def main():

    # Add parser to parse input arguments
    # Neccessary argument to start a program are files with agents, system and actions descriptions
    parser = argparse.ArgumentParser(description='Emulation of Automated Attackers in Cybersecurity')

    parser.add_argument('--agents', metavar='agents', nargs=1, help='an imput file with agents descriptions', required=True)
    parser.add_argument('--system', metavar='system', nargs=1, help='an imput file with system descriptions', required=True)
    parser.add_argument('--actions', metavar='actions', nargs=1, help='an imput file with actions descriptions', required=True)

    args = parser.parse_args()

    print(args.agents[0])

    # Read input arguments and parse json files
    with open(args.actions[0]) as actions_file:
        actions_list = json.loads(actions_file.read())
    with open(args.agents[0]) as agents_file:
        agents_list = json.loads(agents_file.read())
    with open(args.system[0]) as system_file:
        system = json.loads(system_file.read())

    agents = []
    for agent_name in agents_list:
        agent_call = getattr(agent, agent_name)
        # print(agent_call)
        # agents.append(agent.agent(agent_name, agents_list[agent_name]))
        agents.append(agent_call(agents_list[agent_name]))

    network_list = network.network_model(system)

    # actions = []
    # for action_name in actions_list:
        # actions.append(action.action(action_name, actions_list[action_name]) )
        # print(actions_list[action_name])

    # print(actions)
    
    # graf.vizualize(network_list)

    index = 0
    for i in range(len(agents)):
        if agents[i].get_name() == "gray_agent":
            index = i
            break
    
    gray_agent = agents[0]
    
    gray_agent.execute_action("user_login_to_host", ["accountant_workstation", network_list])

    for component in network_list.get_user_components():
        if component.get_name() == "accountant_workstation":
            print(component.get_active_accounts())
    
    gray_agent.execute_action("reboot_host", ["accountant_workstation", network_list])
    
    for component in network_list.get_user_components():
        if component.get_name() == "accountant_workstation":
            print(component.get_active_accounts())
    
    
    gray_agent.add_unread_email("boss")
    gray_agent.add_unread_email("coworker")
    gray_agent.add_unread_email("malicious")
    
    gray_agent.execute_action("open_email", ["accountant_workstation", network_list])

    print(gray_agent.get_unread_emails())
    
    network_list.add_graph(graf.make_network(network_list))
    
    for comp in ["accountant_workstation", "manager_workstation", "developer_workstation"]:
        component = network_list.get_component(comp)
        component.set_status(True)
    
    gray_agent.execute_action("user_login_to_host", ["accountant_workstation", network_list])
    gray_agent.execute_action("open_connection_between_hosts", ["accountant_workstation", "manager_workstation", network_list])

    for comp in ["accountant_workstation", "manager_workstation"]:
        component = network_list.get_component(comp)
        print(component.get_active_connections())

    gray_agent.execute_action("open_connection_between_hosts", ["accountant_workstation", "developer_workstation", network_list])

    for comp in ["accountant_workstation", "developer_workstation"]:
        component = network_list.get_component(comp)
        print(component.get_active_connections())


    gray_agent.execute_action("close_connection_between_hosts", ["accountant_workstation", "manager_workstation", network_list])

    for comp in ["accountant_workstation", "manager_workstation"]:
        component = network_list.get_component(comp)
        print(component.get_active_connections())


    # print(network_list.get_user_components())
    # print(network_list.get_network_components())


main()
