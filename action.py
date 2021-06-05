import random
import networkx

# action: do nothing
# no preconditions
# no postcondition
def do_nothing(agent,args):
    return 1


# action: reboot host
# no preconditions
# flush all credentials and return 1
# in case of error return -1
def reboot_host(agent, args):
    try:
        network = args[0]
        employee = args[1]

        host_name = employee.component
        component = network.get_component(host_name)

        # flush credentials
        component.remove_all_active_accounts()
        return 1

    except:
        return -1


# action: user login to a host
# preconditions: component is active, agent is authorized to log in
# postcondition: agent credentials are stored in component memory
# if the preconditions are satisfied and credentials are stored, return 1
# if the preconditions are not satisfied or error, return -1
def user_login_to_host(agent, args):
    try:
        network = args[0]
        employee = args[1]

        host_name = employee.component
        component = network.get_component(host_name)
        

        # check if employee is loged in in his component
        if employee.name not in component.active_accounts:
            
            # if the component is not active (it has zero active accounts), set it to active
            if component.status == False:
                component.set_status(True)

            # add agent to the list of active account on component
            component.add_active_account(employee.name)
            employee.add_login(component.name)
            # print("Employee {} loged in to component {}".format(employee.name,component.name ))

            return 1

        # if the employee is loged in to his component, he can remotely login to other components he has access to
        elif employee.remote != []:

            # get list of all components employee can remotely access
            not_remotely_loged = [network.get_component(x) for x in employee.remote if employee.name not in network.get_component(x).active_accounts]

            # check if exists any component employee can remotely login to
            if not_remotely_loged != []:

                # chose one component to remotely login to
                chose_remotely_login = agent.strategy.chose_component([not_remotely_loged])

                # if the component is not active (it has zero active accounts), set it to active
                if chose_remotely_login.status == False:
                    chose_remotely_login.set_status(True)

                # add agent to the list of active account on chose_remotely_login
                chose_remotely_login.add_active_account(employee.name)
                employee.add_login(chose_remotely_login.name)
                # print("Employee {} loged in to component {}".format(employee.name,chose_remotely_login.name ))

                return 1

        return 0
    except:
        return -1


# action: open email
# preconditions: employee has unread emails and employee is loged in to his host and employee can remotely connect to mail server
# postconditions: one less unread email, if the read email is malicious, attacker gains access to component
def open_email(agent, args):
    try:
        network = args[0]
        employee = args[1]
        employees = args[2]
        attacker = args[3]["attacker"]

        employee_component = network.get_component(employee.component)

        #check preconditions
        if  employee_component.status == True and \
            employee.name in employee_component.active_accounts and \
            employee.unread_emails != [] and \
            "mail_server" in employee.remote:

            # execute action
            while True:
                random_email = employee.get_random_email()
                if random_email == "": return 0
                elif random_email == "attacker" and not attacker.has_access and employee.priviledge_level == 1:
                    # agent opened malicious email, attacker got access to his station
                    attacker.add_foothold(employee_component)
                    attacker.has_access = True
                    # print("Opened malicious. Attacker got access to component {}".format(employee_component.name))
                    return 1

                elif random_email != "attacker":
                    # agent opened non-malicious email, do nothing
                    # print("\nemail {} read\n".format(random_email))
                    return 1
        return 0
    except:
        return -1


# action: send email
# preconditions: employee is loged in
# postconditions: employee sent email
def send_email(agent, args):
    try:

        network = args[0]
        employee = args[1]
        employees = args[2]

        employee_component = network.get_component(employee.component)
        
        if employee_component.status == True and employee.name in employee_component.active_accounts:
            while True:
                receiver = random.choice(list(employees.values()))
                if receiver != employee: break

            # print("Employee {} sent email to employee {}".format(employee.name, receiver.name))
            receiver.add_unread_email(employee.name)

            return 1
        return 0

    except:
        return -1


# action: browsing the internet
# preconditions: component connected to internet, user is logged in
# postconditions: if the visited website is malicious, attacker gains access
# def browser_internet(agent, host_name, network, attacker):
def browser_internet(agent, args):
    try:
        network = args[0]
        employee = args[1]
        attacker = args[3]["attacker"]

        employee_component = network.get_component(employee.component)

        if employee_component.status == True and employee.name in employee_component.active_accounts:
            # agent is "visiting" random websites
            websites = ["google", "reddit", "news", "malicious", "facebook", "sport", "other random webpage"]
            visited_website = websites[random.randint(0, len(websites)-1)]

            # if the website is malicious, attacker gains access to the system
            if visited_website == "malicious" and not attacker.has_access and employee.priviledge_level == 1:
                attacker.add_foothold(employee_component)
                attacker.has_access = True
                # print("Attacker got access to component {}".format(employee_component.name))

                return 1
        return 0
    except:
        return -1


# action: open a network connection between two hosts
# preconditions: hosts are connected, and host are active, agent has access to host which makes connection
# postcondition: connection is opened
def open_connection_between_hosts(agent, args):

    try:

        network = args[0]
        employee = args[1]
        employees = args[2]

        employees_online = [employees[x] for x in employees if employees[x].active_logins != []]

        if employees_online == []: return 0

        while True:
            employee_to = random.choice(list(employees_online))
            if employee_to != employee: break

        employee_from_component = network.get_component(employee.component)
        employee_to_component = network.get_component(employee_to.component)

        name_from = "\n".join(employee.component.split("_"))
        name_to = "\n".join(employee_to.component.split("_"))

        if employee_to_component.name in employee_from_component.get_connected_components(network) \
            and employee.name in employee_from_component.active_accounts:

            employee_from_component.add_active_connection(employee_to_component.name, (employee.name, employee_to.name))
            employee_to_component.add_active_connection(employee_from_component.name, (employee.name, employee_to.name))

            employee.add_connections(employee_to)
            employee_to.add_connections(employee)
            
            # print("Connection made between hosts {} and {}".format(employee_from_component.name, employee_to_component.name))
            return 1

        return 0
    except:
        return -1


# action: close connection between two hosts
# preconditions: connection exists
# postconditions: connection is terminated
def close_connection_between_hosts(agent, args):

    try:
        network = args[0]
        employee = args[1]
        employees = args[2]

        # get current employee component
        employee_component = network.get_component(employee.component)

        # get acitve connections for current employee and its component
        employee_connections = employee.active_connections
        component_connections = employee_component.active_connections

        if employee.name in employee_component.active_accounts and employee_connections != []:
            employee_close_connection_with = employees[employee_connections[random.randint(0, len(employee_connections)-1)]]
            
            employee_close_connection_with_name = employee_close_connection_with.name
            employee_close_connection_with_component = network.get_component(employee_close_connection_with.component)
            
            employee.remove_connection(employee_close_connection_with_name)
            employee_close_connection_with.remove_connection(employee.name)
            
            employee_component.remove_active_connection(employee_close_connection_with_component, employee.name, employee_close_connection_with_name)
            employee_close_connection_with_component.remove_active_connection(employee_component, employee_close_connection_with_name, employee.name)
            
            # print("Connection closed between employee {} and {}".format(employee.name, employee_close_connection_with_name))
            
            return 1

        return 0
    except:
        return -1


# action: check opened connections on host
# preconditions: agent is defender and has permission to perform check
# postconditions: if connection is opened by attacker, it is terminated
def check_opened_connections(agent, args):

    try:

        network = args[0]
        attacker = args[3]["attacker"]

        have_connections = [x for x in network.user_components if x.active_connections != {}]

        if have_connections == []: return 0

        chosen_component = agent.strategy.chose_component([have_connections])
        component_connection = chosen_component.active_connections

        for connected_component in component_connection:
            if len(component_connection[connected_component]) == 1:
                for connection in component_connection[connected_component]:
                    if "attacker" in connection:
                        connected_component2 = network.get_component(connected_component)
                        # print("\n\nFound attacker in connection between component {} and {}\n".format(chosen_component.name, connected_component2.name))
                        attacker.del_foothold([chosen_component,connected_component2])
                        connected_component2.remove_attacker_connection(chosen_component)
                        chosen_component.remove_attacker_connection(connected_component2)

        return 1

    except:
        return -1


# action: delete account on host
# preconditions: agent is defender and has sufficient priviledge level
# postconditions: account on speficied host is deleted
def delete_account(agent, args):

    try:
        host_name = args[0]
        network = args[1]
        account_name = args[2]

        component = network.get_component(host_name)

        if agent.name == "defender" and agent.priviledge_level == 5:
            return component.remove_active_account(account_name)
        return 0
    except:
        return -1


# action: dump credentials of host X
# preconditions: agent is attacker and has escalated foothold on host X
# postconditions: learn all credentials of active users on host X
def dump_credentials(agent, args):

    try:
        network = args[0]
        attacker = args[3]["attacker"]
        
        if agent.compromise["escalated"] == []: return 0
        
        component = agent.strategy.chose_component([agent.compromise["escalated"]] )

        if agent.name == "attacker" and component in attacker.compromise["escalated"]:

            active_accounts = component.active_accounts
            for account in active_accounts:
                agent.add_knowledge("credentials", account)
            return 1

        return 0

    except:
        return -1


# action: priviledge escalation on host X
# preconditions: agent is attacker and attacker has to have low-level priviledge on host X
# postconditions: priviledge level is increased by 1
def escalate_priviledges(agent, args):

    try:

        network = args[0]
        # get list of all components attacker has foothold on, but did not already escalated priviledges
        footholds_not_escalated = [x for x in agent.compromise["footholds"] if x not in agent.compromise["escalated"]]

        if footholds_not_escalated == []: return 0

        # chose one component to escalate priviledges on
        component = agent.strategy.chose_component([footholds_not_escalated])

        if agent.name == "attacker" and component in agent.compromise["footholds"] \
            and component not in agent.compromise["escalated"]:
            agent.add_compromise("escalated", component)
            # agent.set_priviledge_level(self, host_name, agent.get_priviledge_level(host_name) + 1)
            return 1
        return 0
    except:
        return -1


# action: enumerate host X
# preconditions: agent is attacker and agent has escalated priviledges on host X, and agent did not already enumerated host X
# postconditions: agent has enumerated host X, agent knows all active connections of host X
def enumerate_host(agent, args):

    try:

        network = args[0]
        attacker = args[3]["attacker"]

        # get list of all components attacker has foothold on, but did not already enumerated
        footholds_not_enumerated = [x for x in agent.compromise["escalated"] if x not in agent.compromise["enumerated"] ]

        if footholds_not_enumerated == []: return 0

        # chose one component to enumerate
        component = agent.strategy.chose_component([footholds_not_enumerated])

        if agent.name == "attacker" and component in attacker.compromise["escalated"] \
            and component not in attacker.compromise["enumerated"]:

            agent.add_compromise("enumerated", component)
            for active_connection in component.active_connections:
                agent.add_knowledge("active_connections", (component.name, active_connection))
            for connected_component in component.get_connected_components(network):
                agent.add_knowledge("connected", (component.name, connected_component))

            return 1

        return 0

    except:
        return -1


# action: exfiltrate data from host X
# preconditions: agent is attacker and agent has escalated priviledges on host X, enumerated host X and did not already exfiltrated host X
# postconditions: agent exfiltrated host X
def exfiltrate_data(agent, args):

    try:

        network = args[0]
        attacker = args[3]["attacker"]

        # get all possible components to extract data from
        # if the component is enumerated, it was also escalated
        possible_components = [x for x in agent.compromise["escalated"] if x not in agent.compromise["exfiltrated"]]

        if possible_components == []: return 0

        # chose one component to exfiltrate data from
        component = agent.strategy.chose_component([possible_components])

        if agent.name == "attacker" and component not in agent.compromise["exfiltrated"]:

            agent.add_compromise("exfiltrated", component)
            # print("Host {} exfiltrated".format(component.name))
            return 1

        return 0

    except:
        return -1


# action: lateral movement to host X using account A
# preconditions: agent is attacker and agent has foothold on host Y, know X and Y are connected, knows credentials of A
#    have escalated priviledges on Y, know that A can remotely login to X, and not have foothold on X
# postconditions: have foothold on X
def lateral_movement(agent,args):

    try:

        network = args[0]
        employees = args[2]
        attacker = args[3]["attacker"]

        # get all known credentials
        known_credentials = agent.knowledge["credentials"]

        # get list of all components attacker has probed accounts on, but has no foothold
        probed_no_foothold = [ x for x in agent.compromise["probed_accounts"] if x not in agent.compromise["footholds"] ]

        for component_probed in probed_no_foothold:

            for component, accounts in agent.knowledge["local_admins"]:

                # check if the agent has probed component
                if component in agent.compromise["probed_accounts"]:

                    # get known credentials which can remotely login to component
                    known_credentials_for_component = []
                    for account in accounts:
                        if account in known_credentials:
                            known_credentials_for_component.append(account)

                    if known_credentials_for_component == []: return 0

                    random_credential = agent.strategy.chose_component([known_credentials_for_component])

                    # get component which is connected to component, and which agent has foothold and escalated priviledges on
                    connected_probed_no_foothold = set()
                    for connection in agent.knowledge["connected"]:
                        component_X, component_Y = connection
                        component_X = network.get_component(component_X)
                        component_Y = network.get_component(component_Y)
                        if component_X in agent.compromise["footholds"] \
                            and component_X in agent.compromise["escalated"] \
                            and component_Y not in agent.compromise["footholds"] : 
                            connected_probed_no_foothold.add(component_X)
                        elif component_Y in agent.compromise["footholds"] \
                            and component_Y in agent.compromise["escalated"] \
                            and component_X not in agent.compromise["footholds"]:
                            connected_probed_no_foothold.add(component_Y)

                    if connected_probed_no_foothold == set(): return 0

                    # get one component from which we will perform lateral movement
                    source_component = agent.strategy.chose_component([list(connected_probed_no_foothold)])

                    if agent.name == "attacker" \
                        and source_component in agent.compromise["footholds"] \
                        and source_component in agent.compromise["escalated"] \
                        and component.name in source_component.get_connected_components(network) \
                        and employees[random_credential].name in agent.knowledge["credentials"] \
                        and (random_credential, component) in agent.knowledge["remote"] \
                        and component not in agent.compromise["footholds"]:

                        # print("We have an account which can log in to other component")
                        # print("Perform lateral movement from component {} to component {} using credentials of {}".format(source_component.name, component.name, random_credential))

                        agent.add_compromise("footholds", component)

                        # check if connection between connected component and vulnerable component exists
                        # if the connection does not exist, create new connection
                        if component not in list(source_component.active_connections.keys()):
                            # print("\n\nConnection does not exist, create new one")
                            source_component.add_active_connection(component.name, (agent.name,))
                            component.add_active_connection(source_component.name, (agent.name,))

                        return 1

                    # print("Failed to perform lateral movement from component {} to component {} using credentials of {}".format(source_component.name, component.name, random_credential))

        return 0
    except:
        return -1


# function to check if some of the components are exploitable with one exploit in exploit toolbox
def check_if_vulnerable(components_not_exploited, exploits, network, agent):

    for tool in exploits:
        vulnerable_software = exploits[tool]

        copy_components_not_exploited = components_not_exploited[:]
        while True:
            chosen_component = agent.strategy.chose_component([copy_components_not_exploited])
            component_index = copy_components_not_exploited.index(chosen_component)
            del copy_components_not_exploited[component_index]

            chosen_component = network.get_component(chosen_component)
            if vulnerable_software in chosen_component.software:

                # print("Successfully exploited software {} on component {} using exploit {}".format(vulnerable_software, chosen_component.name, tool))
                return (vulnerable_software, chosen_component, tool)

            elif copy_components_not_exploited == []:
                break

    return False

# action: run Exploit E on host X
# preconditions: agent is attacker, agent has foothold on Y, know X and Y are connected, does not have foothold on X, 
#    and did not tried exploiting X with E before
# postconditions: have foothold on X if X is vulnerable with E
def run_exploit(agent, args):

    try:

        network = args[0]
        agents = args[3]

        # get list of components attacker has foothold on
        has_foothold = agent.compromise["footholds"]

        # get list of all components that the attacker does not have foothold on
        # but are connected to the components to which attacker has foothold on
        connected_no_foothold = set()
        for connection in agent.knowledge["connected"]:
            component_X, component_Y = connection
            component_X = network.get_component(component_X)
            component_Y = network.get_component(component_Y)
            if component_X in has_foothold and component_Y not in has_foothold: connected_no_foothold.add(component_Y.name)
            elif component_Y in has_foothold and component_X not in has_foothold: connected_no_foothold.add(component_X.name)

        # get list of all components attacker did not tried to exploit before
        components_not_exploited = [x for x in connected_no_foothold if x not in agent.compromise["exploited"]]

        if agent.name == "attacker" and components_not_exploited != [] and agent.tools.get("exploits", {}) != {}:

            check_components = check_if_vulnerable(components_not_exploited, agent.tools["exploits"], network, agent)
            if check_components != False:
                vulnerable_software, vulnerable_component, exploit = check_components

                agent.add_compromise("exploited", vulnerable_component)
                agent.add_compromise("footholds", vulnerable_component)

                for connection in agent.knowledge["connected"]:
                    component_X, component_Y = connection
                    component_X = network.get_component(component_X)
                    component_Y = network.get_component(component_Y)
                    if component_Y == vulnerable_component:
                        connected_component = component_X
                        break
                    elif component_X == vulnerable_component:
                        connected_component = component_Y
                        break

                # print("Attacker got access to component {}".format(vulnerable_component.name))

                # check if connection between connected component and vulnerable component exists
                # if the connection does not exist, create new connection
                if vulnerable_component not in list(connected_component.active_connections.keys()):
                    # print("\nConnection does not exist, create a new ones")
                    connected_component.add_active_connection(vulnerable_component.name, (agent.name,))
                    vulnerable_component.add_active_connection(connected_component.name, (agent.name,))

            return 1

        return 0

    except:
        return -1


# action: discover admin accounts on host X
# preconditions: agent is attacker, agent has foothold on Y, Y and X are connected, 
#    agent does not have foothold on X or probed accounts on X
# postconditions: agents probed accounts on host X, knows admin accounts on X
def account_discovery(agent, args):

    try:

        network = args[0]
        attacker = args[3]["attacker"]

        # get list of components attacker has foothold on
        has_foothold = agent.compromise["footholds"]

        # get list of components attacker has probed accounts to
        has_probed = agent.compromise["probed_accounts"]

        # get list of all components that the attacker does not have foothold on
        # but are connected to the components to which attacker has foothold on
        connected_no_foothold_or_probed = set()
        for connection in agent.knowledge["connected"]:
            component_X, component_Y = connection
            component_X = network.get_component(component_X)
            component_Y = network.get_component(component_Y)
            if component_X in has_foothold and not (component_Y in has_foothold or component_Y in has_probed): 
                connected_no_foothold_or_probed.add(component_Y)
            elif component_Y in has_foothold and not (component_X in has_foothold or component_X in has_probed):
                connected_no_foothold_or_probed.add(component_X)


        if agent.name == "attacker" and connected_no_foothold_or_probed != set():

            # chose one component to probe admin accounts on
            component_to_probe = agent.strategy.chose_component([list(connected_no_foothold_or_probed)])

            # get component which is connected to chosen component to probe accounts 
            for connection in agent.knowledge["connected"]:
                component_X, component_Y = connection
                component_X = network.get_component(component_X)
                component_Y = network.get_component(component_Y)
                if component_X == component_to_probe:
                    connected_to_probe = component_Y
                    break
                elif component_Y == component_to_probe:
                    connected_to_probe = component_X
                    break

            # check preconditions
            if connected_to_probe in agent.compromise["footholds"] \
                and component_to_probe.name in connected_to_probe.get_connected_components(network) \
                and component_to_probe not in agent.compromise["footholds"] \
                and component_to_probe not in agent.compromise["probed_accounts"]:

                # make postconditions
                agent.add_compromise("probed_accounts", component_to_probe)
                agent.add_knowledge("local_admins", (component_to_probe, component_to_probe.admin_accounts) )
                for account in component_to_probe.admin_accounts:
                    # print(account, component_to_probe.name)
                    agent.add_knowledge("remote", (account, component_to_probe))

                return 1
            return 0

        return 0

    except:
        return -1


# action: initiall access
# preconditions: attacker has not access
# postconditions: attacker sent malicious emails to random employees
def initial_access(agent, args):

    try:

        if agent.name == "attacker" and not agent.has_access:
            network = args[0]
            employees = args[2]

            sent_emails = set()
            random_employees = random.sample(list(employees.values()), (len(employees) // 5))

            for random_employee in random_employees:
                random_employee.add_unread_email(agent.name)

            return 1
        return 0
    except:
        return -1


''' action template
# action: [name of the action]
# preconditions: [preconditions that needs to be satisfied to perform action]
# postconditions: [postconditions that happen once the action is successfully executed]
def action_name(agent, args):

    args = [
        network,
        employee/agent who is executing action,
        list of all employees,
        list of all agents
       ]
    network = args[0]
    employee = args[1]
    employees = args[2]
    agents = args[3]
    
    try:

        get arguments

        if preconditions:
            execute action
            return 1
        # if the preconditions are not satisfied
        return 0
    except:
        # error happened while trying to execute action
        return -1
'''













