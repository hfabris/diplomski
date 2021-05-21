import random
import networkx

# action: reboot host
# no preconditions
# flush all credentials and return 1
# in case of error return -1
def reboot_host(agent, args):
    try:
        network = args[0]
        employee = args[1]

        host_name = employee.get_component()
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
        # host_name = args[0]
        network = args[0]
        employee = args[1]

        host_name = employee.get_component()
        component = network.get_component(host_name)

        if (not component.is_account_active(employee.get_name())): #and (host_name in agent.get_knowledge()) :
            
            # if the component is not active (it has zero active accounts), set it to active
            if component.get_status() == False:
                component.set_status(True)
            # add agent to the list of active account on component
            component.add_active_account(employee.get_name())

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

        employee_component = network.get_component(employee.get_component())
    
        #check preconditions
        if  employee_component.get_status() == True and \
            employee_component.is_account_active(employee.get_name()) and \
            employee.get_unread_emails() != [] and \
            "mail_server" in employee.remote0:

            # open connection between employee host and mail server
            # mail_server = network.get_component("mail_server")

            # employee_component.add_active_connection(mail_server.get_name(), (employee.get_name(), employee_to.get_name()))
            # mail_server.add_active_connection(employee_component.get_name(), (employee.get_name(), employee_to.get_name()))
            
            # employee.add_connections(employee_to)
            # employee_to.add_connections(employee)

            # execute action
            while True:
                # oldest_unread = employee.get_oldest_unread_email()
                random_email = employee.get_random_email()
                if random_email == "attacker" and not attacker.has_access:
                    attacker.add_foothold(employee_component)
                    print("Opened malicious. Attacker got access to component {}".format(employee_component.name))
                    print(attacker.has_access)
                    return 1
                    # component = network.get_component(host_name)
                    # attacker.add_access(component)
                    # agent opened malicious email, attacker got access to his station
                elif random_email != "attacker":
                    print("\nemail {} read\n".format(random_email))
                    # agent opened non-malicious email, do nothing
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

        employee_component = network.get_component(employee.get_component())
        
        if employee_component.get_status() == True and employee_component.is_account_active(employee.get_name()):
            while True:
                receiver = random.choice(list(employees.values()))
                if receiver != employee: break

            print("Employee {} sent email to employee {}".format(employee.get_name(), receiver.get_name()))
            receiver.add_unread_email(employee.get_name())

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

        employee_component = network.get_component(employee.get_component())

        if employee_component.get_status() == True and employee_component.is_account_active(employee.get_name()):
            # agent is "visiting" random websites
            websites = ["google", "reddit", "news", "malicious", "facebook", "sport", "other random webpage"]
            visited_website = websites[random.randint(0, len(websites)-1)]
            print('Employee "{}" is browsing {}'.format(employee.get_name(), visited_website))

            # if the website is malicious, attacker gains access to the system
            if visited_website == "malicious" and not attacker.has_access:
                # component = network.get_component(host_name)
                # attacker.add_access(component)
                attacker.add_foothold(employee_component)
                print(attacker.has_access)
                print("Attacker got access to component {}".format(employee_component.name))
                print(attacker.has_access)

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

        while True:
            employee_to = random.choice(list(employees.values()))
            if employee_to != employee: break

        employee_from_component = network.get_component(employee.get_component())
        employee_to_component = network.get_component(employee_to.get_component())

        name_from = "\n".join(employee.get_component().split("_"))
        name_to = "\n".join(employee_to.get_component().split("_"))

        if networkx.algorithms.shortest_paths.generic.has_path(network.get_graph(), name_from, name_to) \
            and employee_from_component.get_status() and employee_to_component.get_status() \
            and employee_from_component.is_account_active(employee.get_name()):

            employee_from_component.add_active_connection(employee_to_component.get_name(), (employee.get_name(), employee_to.get_name()))
            employee_to_component.add_active_connection(employee_from_component.get_name(), (employee.get_name(), employee_to.get_name()))
            
            employee.add_connections(employee_to)
            employee_to.add_connections(employee)
            
            # print("Connection made between hosts {} and {}".format(employee_from_component.get_name(), employee_to_component.get_name()))
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
        employee_component = network.get_component(employee.get_component())

        # get acitve connections for current employee and its component
        employee_connections = employee.get_active_connections()
        component_connections = employee_component.get_active_connections()

        if employee_component.is_account_active(employee.get_name()) and employee_connections != []:
            employee_close_connection_with = employees[employee_connections[random.randint(0, len(employee_connections)-1)]]
            
            employee_close_connection_with_name = employee_close_connection_with.get_name()
            employee_close_connection_with_component = network.get_component(employee_close_connection_with.get_component())
            
            employee.remove_connection(employee_close_connection_with_name)
            employee_close_connection_with.remove_connection(employee.get_name())
            
            employee_component.remove_active_connection(employee_close_connection_with_component, employee.get_name(), employee_close_connection_with_name)
            employee_close_connection_with_component.remove_active_connection(employee_component, employee_close_connection_with_name, employee.get_name())
            
            print("Connection closed between employee {} and {}".format(employee.get_name(), employee_close_connection_with_name))
            
            return 1

        return 0
    except:
        return -1


# action: check opened connections on host
# preconditions: agent is defender and has permission to perform check
# postconditions: if connection is opened by attacker, it is terminated
def check_opened_connections(agent, args):

    try:
        host_name = args[0]
        network = args[1]

        component = network.get_component(host_name)
        component_connections = component.get_active_connections()
        if agent.name == "defender" and agent.get_priviledge_level() == 5:
            for connected_component, initiator in component_connections:
                if initiator == "attacker":
                    component.remove_active_connection(connected_component, initiator)
                    connected_component.remove_active_connection(component, initiator)
            return 1
        return 0
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
        component = agent.strategy.chose_component([agent.compromise["escalated"]] )

        attacker = args[3]["attacker"]

        if agent.name == "attacker" and component in attacker.compromise["escalated"]:

            active_accounts = component.get_active_accounts()
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

        # chose one component to enumerate
        component = agent.strategy.chose_component([footholds_not_enumerated])

        if agent.name == "attacker" and component in attacker.compromise["escalated"] \
            and component not in attacker.compromise["enumerated"]:

            agent.add_compromise("enumerated", component)
            for active_connection in component.active_connections:
                agent.add_knowledge("active_connections", (component.name, active_connection))
            for connected_component in component.connected_components:
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

        # chose one component to exfiltrate data from
        component = agent.strategy.chose_component([possible_components])

        if agent.name == "attacker" and component not in agent.compromise["exfiltrated"]:

            agent.add_compromise("exfiltrated", component)
            print("Host {} exfiltrated".format(component.name))
            return 1

        return 0

    except:
        return -1


# action: lateral movement to host X using account A
# preconditions: agent is attacker and agent has foothold on host Y, know X and Y are connected, knows credentials of A
#    escalated priviledges on Y, know that A can remotely login to X, and not have foothold on X# preconditions: agent is attacker and agent has foothold on host Y, know X and Y are connected, knows credentials of A
# postconditions: have foothold on X
def lateral_movement(agent,args):

    try:

        network = args[0]
        attacker = args[3]["attacker"]

        # get all known credentials
        known_credentials = agent.knowledge["credentials"]

        # for all accounts in known credentials, get list of components those accounts can remotely login
        remote_components = [x for x in agent.knowledge["remote"] if x[0] in known_credentials]

        # get list of all components that are connected to those we want to remotely login to
        known_connected = [x for x in agent.knowledge["connected"] if x in remote_components]
        # known_connected = []
        # for connection in agent.knowledge["connected"]:
            # component_X, component_Y = connection
            # if component_X in remote_components: known_connected.append(component_Y)
            # elif component_Y in remote_components: known_connected.append(component_X)

        # get list of all components the attacker has no foothold on, and to which we have account credentials to remotely login
        no_foothold = [x for x in remote_components if x not in agent.compromise["footholds"]]
        
        # chose one component to remotely login to and get a foothold
        component_to_move = agent.strategy.chose_component([no_foothold])
        
        # get list of components which are connected to component we want to move to
        connected_components = []
        for connection in known_connected:
            component_X, component_Y = connection
            if component_X == component_to_move.name: connected_components.append(component_Y)
            elif component_Y == component_to_move.name: connected_components.append(component_X)

        # if agent.name == "attacker" and component in attacker.compromise["footholds"] \
            # and component in 


        return 0
    except:
        return -1


# action: run Exploit E on host X
# preconditions: agent is attacker, agent has foothold on Y, know X and Y are connected, does not have foothold on X, 
#    and did not tried exploiting X with E before
# postconditions: have foothold on X if X is vulnerable with E
def run_exploit(agent, args):

    try:

        network = args[0]
        agents = args[3]

        print(agent.tools.get("exploits", {}))

        # get list of components attacker has foothold on
        has_foothold = agent.compromise["footholds"]

        # get list of all components that the attacker does not have foothold on
        # but are connected to the components to which attacker has foothold on
        connected_no_foothold = []
        for connection in agent.knowledge["connected"]:
            component_X, component_Y = connection
            component_X = network.get_component(component_X)
            component_Y = network.get_component(component_Y)
            if component_X in has_foothold and component_Y.name not in has_foothold: connected_no_foothold.append(component_Y.name)
            elif component_Y in has_foothold and component_X.name not in has_foothold: connected_no_foothold.append(component_X.name)

        # get list of all components attacker did not tried to exploit before
        components_not_exploited = [x for x in connected_no_foothold if x not in agent.compromise["exploited"]]

        if agent.name == "attacker" and components_not_exploited != [] and agent.tools.get("exploits", {}) != {}:

            for tool in agent.tools["exploits"]:
                vulnerable_software = agent.tools["exploits"][tool]
                
                for component in components_not_exploited:
                    component = network.get_component(component)
                    # if vulnerable_software in component.software:
                        
                    print(component.name)
                    print(component.software)



            
            
            return 1

        return 0    


        host_X_name = args[0]
        host_Y_name = args[1]
        network = args[2]
        exploit = args[3]

        name_Y = "\n".join(host_X_name.split("_"))
        name_X = "\n".join(host_Y_name.split("_"))

        if agent.get_name() == "attacker" and host_Y_name in agent.get_knowledge()["established_footholds"] \
            and ( (host_X_name, host_Y_name) in agent.get_knowledge()["connected"] or (host_Y_name, host_X_name) in agent.get_knowledge()["connected"] ) \
            and host_X_name not in agent.get_knowledge()["established_footholds"] :

            component_X = network.get_component(host_X_name)
            if component_X.is_vulnerable(exploit):
                agent.add_foothold(component_X)
                return 1
            return 2

        return 0

    except:
        return -1


# action: discover admin accounts on host X
# preconditions: agent is attacker, agent has foothold on Y, Y and X are connected, agent does not have foothold on X or probed accounts on X
# postconditions: agents probed accounts on host X, knows admin accounts on X
def account_discovery(agent, args):

    try:

        host_X_name = args[0]
        host_Y_name = args[1]
        network = args[2]

        name_X = "\n".join(host_from.split("_"))
        name_Y = "\n".join(host_to.split("_"))

        if agent.get_name() == "attacker" and ( host_Y_name in agent.get_knowledge()["established_footholds"] ) \
            and networkx.algorithms.shortest_paths.generic.has_path(network.get_graph(), name_X, name_Y) \
            and ( host_X_name not in agent.get_knowledge()["established_footholds"] ) \
            and ( host_X_name in agent.get_knowledge()["probed_accounts"] ):

            agent.add_knowledge("probed_accounts", host_X_name)

            component_X = network.get_component(host_X_name)
            agent.add_knowledge("local_admins", (component_X.get_name(), component_X.get_admins() ))
            return 1

        return 0

    except:
        return -1


# action: initiall access
# preconditions: None
# postconditions: attacker sent malicious emails to random employees
def initial_access(agent, args):

    try:

        network = args[0]
        employees = args[2]

        sent_emails = set()
        random_employees = random.sample(list(employees.values()), (len(employees) // 5))

        for random_employee in random_employees:
            random_employee.add_unread_email(agent.name)

        return 1
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













