import json
import argparse

import network
import agent
import action
import graf
import random

import strategies

# python main.py --agents agent.txt --actions actions.txt --system model_sustava.txt
# python main.py --agents agent.txt --system model_sustava.txt
def main():

    # Add parser to parse input arguments
    # Neccessary argument to start a program are files with agents, system and actions descriptions
    parser = argparse.ArgumentParser(description='Emulation of Automated Attackers in Cybersecurity')
    parser.add_argument('--system', metavar='system', nargs=1, help='an imput file with system descriptions', required=True)
    parser.add_argument('--agents', metavar='agents', nargs=1, help='an input file with agents descriptions', required=True)
    # parser.add_argument('--actions', metavar='actions', nargs=1, help='an imput file with actions descriptions', required=True)

    args = parser.parse_args()

    print(args.agents[0])

    # Read input arguments and parse json files
    # with open(args.actions[0]) as actions_file:
        # actions_list = json.loads(actions_file.read())
    with open(args.agents[0]) as agents_file:
        agents_list = json.loads(agents_file.read())
    with open(args.system[0]) as system_file:
        system = json.loads(system_file.read())

    agents = {}
    for agent_name in agents_list:
        agent_call = getattr(agent, agent_name)
        agents[agent_name] = agent_call(agents_list[agent_name])

    network_list = network.network_model(system)
    network_list.add_graph(graf.make_network(network_list))

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
                info["priviledge_level"] = user_component["priviledge_level"]
                info["domain"] = user_component["domain"]
                info["remote"] = user_component["remote"]
                employee = agent.employee(info)
                employees[employee.name] = employee


    for component in network_list.user_components:
        if component.administrators != []:
            component.add_administrator_accounts(employees)
    
    # print(employees, len(employees))

    random_employee = random.choice(list(employees.values()))
    # print(random_employee.name, random_employee.get_component())

    random_component = network_list.get_component(random_employee.component)
    
    # for component in network_list.get_user_components():  
        # print(component.get_status(), component.get_active_accounts())

    gray = agents["gray_agent"]
    attacker = agents["attacker"]

    # login_employees = []
    # login 50% of all employees in the network
    # for employee in random.sample(list(employees.keys()), (len(employees) // 2)):
        # employee = employees[employee]
        # gray.execute_action("user_login_to_host", [network_list, employee, employees, agents])
        # login_employees.append(login_employees)

    for component in network_list.user_components:
        print(component.name, component.status, component.active_connections)


    # for i in range(5):
        # for employee in employees:
            # employee = employees[employee]
            
            # print("\n{}".format(employee.name))
            # action_list = gray.chose_action(network_list)
            # action_return = gray.execute_action(action_list, [network_list, employee, employees, agents])
            # if action_return == 0:
                # print("Nothing executed")
        # attacker.execute_action(["initial_access"], [network_list, employee, employees, agents])
        

    # print("\n" * 5)

    # for component in network_list.user_components:
        # print(component.name, component.status, component.active_connections)

    empl = employees["System administrator 1"]
    gray.execute_action(["user_login_to_host"], [network_list, empl, employees, agents])
    gray.execute_action(["browser_internet"], [network_list, empl, employees, agents])
    gray.execute_action(["open_connection_between_hosts"], [network_list, empl, employees, agents])
    print(empl.remote)
    print(empl.component)

    print(attacker)
    if attacker.compromise["footholds"] != []:
        print("attacker has {} footholds".format(len(attacker.compromise["footholds"])))
        
        attacker.execute_action(["escalate_priviledges"], [network_list, employee, employees, agents])
        attacker.execute_action(["enumerate_host"], [network_list, employee, employees, agents])
        attacker.execute_action(["dump_credentials"], [network_list, employee, employees, agents])
        attacker.execute_action(["exfiltrate_data"], [network_list, employee, employees, agents])
        attacker.execute_action(["run_exploit"], [network_list, employee, employees, agents])
        print(attacker.execute_action(["account_discovery"], [network_list, employee, employees, agents]))
        print(attacker.execute_action(["lateral_movement"], [network_list, employee, employees, agents]))

    print("\n"*3)

    print(attacker.compromise)
    print(attacker.knowledge)
    print(attacker.has_access)
    

    # for component in network_list.user_components:
        # print(component.admin_accounts)
    


    # for c in network_list.get_component(empl.component).active_connections.keys():
        # c = network_list.get_component(c)
        # c2 = network_list.get_component(empl.component)
        # attacker.add_foothold( c )
        
        # c.add_active_connection(c2.name, (empl.name, "attacker"))
        # c2.add_active_connection(c.name, (empl.name, "attacker"))

    # print(network_list.get_component(empl.component).active_connections)
    # print("\n"*5)
    
    # print(attacker.compromise["footholds"])


    # defender = agents["defender"]
    # print(defender)
    # defender.execute_action(["check_opened_connections"], [network_list, empl, employees, agents])


    # print(attacker.compromise["footholds"])
    # print(network_list.get_component(empl.component).active_connections)
    # print(attacker.compromise)
    
    
    
    
    
    
    # print(network_list.get_component(empl.component).active_connections.keys)
    # print(network_list.get_component(empl.component).active_connections.keys)
    
    
    # for user_compo in network_list.user_components:
        # print(user_compo.active_connections)
   
    # print(employees)
    
    # for employee in employees:
        # print(employees[employee].remote)
    
    # for user_comp in network_list.user_components:
        # print(user_comp.software)
        # print(employee.name, action_return)
        # print(employee.name, action_return)
        
        # print(employee)
        # print(gray.chose_action(network_list))
        
        # gray.execute_action("user_login_to_host", [network_list, employee, employees])
        # gray.execute_action("send_email", [network_list, employee, employees])
        
        # gray.execute_action("open_connection_between_hosts", [network_list, employee, employees])
        # print(network_list.get_component(employee.get_component()).get_active_accounts())
                
        # print("\n\n")
        # print("Employee {} has {} unread emails".format(employee.name, len(employee.get_unread_emails())))
        # gray.execute_action("open_email", [network_list, employee, employees])
        
        # print("Employee {} has {} unread emails".format(employee.name, len(employee.get_unread_emails())))


    # for employee in employees:
        # employee = employees[employee]
        # gray.execute_action("reboot_host", [network_list, employee])


    # for component in network_list.get_user_components():  
        # print(component.get_status(), component.get_active_accounts(), component.get_active_connections())
    # strategy_name = getattr(strategies, gray.get_strategy())
    # strategy_instance = strategy_name(gray.get_actions(), network_list) 

    # for employee in employees:
        # print("Start component")
        # employee = employees[employee]
        # print(employee.get_active_connections(), employee.name)
        # print(network_list.get_component(employee.get_component()).get_active_connections())
        # sum += len(employee.get_active_connections())
        # print(gray.execute_action("close_connection_between_hosts", [network_list, employee, employees]))
        # gray.execute_action("close_connection_between_hosts", [network_list, employee, employees])
    
        # print(employee.get_active_connections(), employee.name)
        # print(network_list.get_component(employee.get_component()).get_active_connections())
        # print("\n\n")


    # for i in range(5):
        # print("Round {}:".format(i+1))
        # for agent_name in agents:

            # action_executed = False
            # agent_name = agents[agent_name]

            # while True:
                # if action_executed: break
            
                # action_name = agent_name.chose_action()
                # action_return = agent_name.execute_action(action_name, [network_list]) 

                # if action_return == 1:
                    # action_executed = True
                    # print("{} -> {}".format(agent_name.name, action_name) )
                # elif action_return == -1:
                    # print("Error while executing action {}".format(action_name))

        # print("\n\n")


    # actions = []
    # for action_name in actions_list:
        # actions.append(action.action(action_name, actions_list[action_name]) )
        # print(actions_list[action_name])

    # print(actions)
    
    # graf.vizualize(network_list)

    
   # gray_agent = agents[0]
    
    # gray_agent.execute_action("user_login_to_host", ["accountant_workstation", network_list])

    # for component in network_list.get_user_components():
        # if component.name == "accountant_workstation":
            # print(component.get_active_accounts())
    
    # gray_agent.execute_action("reboot_host", ["accountant_workstation", network_list])
    
    # for component in network_list.get_user_components():
        # if component.name == "accountant_workstation":
            # print(component.get_active_accounts())
    
    
    # gray_agent.add_unread_email("boss")
    # gray_agent.add_unread_email("coworker")
    # gray_agent.add_unread_email("malicious")
    
    # gray_agent.execute_action("open_email", ["accountant_workstation", network_list])

    # print(gray_agent.get_unread_emails())
    
    # network_list.add_graph(graf.make_network(network_list))
    
    # for comp in ["accountant_workstation", "manager_workstation", "developer_workstation"]:
        # component = network_list.get_component(comp)
        # component.set_status(True)
    
    # gray_agent.execute_action("user_login_to_host", ["accountant_workstation", network_list])
    # gray_agent.execute_action("open_connection_between_hosts", ["accountant_workstation", "manager_workstation", network_list])

    # for comp in ["accountant_workstation", "manager_workstation"]:
        # component = network_list.get_component(comp)
        # print(component.get_active_connections())

    # gray_agent.execute_action("open_connection_between_hosts", ["accountant_workstation", "developer_workstation", network_list])

    # for comp in ["accountant_workstation", "developer_workstation"]:
        # component = network_list.get_component(comp)
        # print(component.get_active_connections())


    # gray_agent.execute_action("close_connection_between_hosts", ["accountant_workstation", "manager_workstation", network_list])

    # for comp in ["accountant_workstation", "manager_workstation"]:
        # component = network_list.get_component(comp)
        # print(component.get_active_connections())


    # print(network_list.get_user_components())
    # print(network_list.get_network_components())


main()
