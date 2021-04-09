import json
import argparse
import network
import agent
import action


# python main.py --agents agent.txt --actions actions.txt --system model_sustava.txt
def main():
    parser = argparse.ArgumentParser(description='Emulation of Automated Attackers in Cybersecurity')

    parser.add_argument('--agents', metavar='agents', nargs=1, help='an imput file with agents descriptions', required=True)
    parser.add_argument('--system', metavar='system', nargs=1, help='an imput file with system descriptions', required=True)
    parser.add_argument('--actions', metavar='actions', nargs=1, help='an imput file with actions descriptions', required=True)

    args = parser.parse_args()

    print(args.agents[0])

    with open(args.actions[0]) as actions_file:
        actions_list = json.loads(actions_file.read())
    with open(args.agents[0]) as agents_file:
        agents_list = json.loads(agents_file.read())
    with open(args.system[0]) as system_file:
        system = json.loads(system_file.read())

    agents = []
    for agent_name in agents_list:
        agents.append(agent.agent(agent_name, agents_list[agent_name]))

    network_list = network.network_model(system)

    actions = []
    for action_name in actions_list:
        actions.append(action.action(action_name, actions_list[action_name]) )
        # print(actions_list[action_name])

    print(actions)

    # for agent_name in agents:
        # print(agent_name.chose_action())

    # print(network_list.get_user_components())
    # print(network_list.get_network_components())


main()
