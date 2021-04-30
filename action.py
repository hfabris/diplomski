import random
import networkx

# action: reboot host
# no preconditions
# flush all credentials and return 1
# in case of error return -1
def reboot_host(agent, args):
    try:
        host_name = args[0]
        network = args[1]

        component = network.get_component(host_name)

        # flush credentials
        for account in component.get_active_accounts():
            component.remove_active_account(account)
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
        host_name = args[0]
        network = args[1]

        component = network.get_component(host_name)

        if (not component.is_account_active(agent.get_name())) and (host_name in agent.get_knowledge()) :
            
            # if the component is not active (it has zero active accounts), set it to active
            if component.get_status() == False:
                component.set_status(True)
            # add agent to the list of active account on component
            component.add_active_account(agent)

            return 1
        return 0
    except:
        return -1


# action: open email
# preconditions: agent has unread emails
# postconditions: one less unread email, if the read email is malicious, attacker gains access to component
def open_email(agent, args):
    try:
        host_name = args[0]
        network = args[1]

        assert agent.name == "gray_agent" or agent.name == "defender"

        #check preconditions
        if agent.get_unread_emails != 0:
            # execute action
            while True:
                oldest_unread = agent.get_oldest_unread_email()
                if oldest_unread == "malicious" and random.randint(0,100) % 5 == 0:
                    print("opened malicious")
                    return 1
                    # component = network.get_component(host_name)
                    # attacker.add_access(component)
                    # agent opened malicious email, attacker got access to his station
                elif oldest_unread != "malicious":
                    print("email read")
                    # agent opened non-malicious email, do nothing
                    return 1
                else:
                    agent.add_unread_email(oldest_unread)
    except:
        return -1
    return -1


# action: browsing the internet
# preconditions: component connected to internet
# postconditions: if the visited website is malicious, attacker gains access
# def browser_internet(agent, host_name, network, attacker):
def browser_internet(agent, args):
    try:
        host_name = args[0]
        network = args[1]

        # agent is "visiting" random websites
        websites = ["google", "reddit", "news", "malicious", "facebook", "sport", "other random webpage"]
        visited_website = websites[random.randint(0, len(websites)-1)]
        print("Agent is browsing {}".format(visited_website))

        # if the website is malicious, attacker gains access to the system
        if visited_website == "malicious":
            # component = network.get_component(host_name)
            # attacker.add_access(component)
            print("Attacker got access to component {}".format(host_name))

        return 1
    except:
        return -1


# action: open a network connection between two hosts
# preconditions: hosts are connected, and host are active, agent has access to host which makes connection
# postcondition: connection is opened
def open_connection_between_hosts(agent, args):

    try:

        host_from = args[0]
        host_to = args[1]
        network = args[2]

        component_from = network.get_component(host_from)
        component_to = network.get_component(host_to)
        
        name_from = "\n".join(host_from.split("_"))
        name_to = "\n".join(host_to.split("_"))

        if networkx.algorithms.shortest_paths.generic.has_path(network.get_graph(), name_from, name_to) and \
            component_from.get_status() and component_to.get_status() and component_from.is_account_active(agent):
            print("Connection made between hosts {} and {}".format(component_from.get_name(), component_to.get_name()))
            component_from.add_active_connection(component_to.get_name(), agent)
            component_to.add_active_connection(component_from.get_name(), agent)
            return 1
        return 0
    except:
        return -1


# action: close connection between two hosts
# preconditions: connection exists
# postconditions: connection is terminated
def close_connection_between_hosts(agent, args):

    try:
        host_from = args[0]
        host_to = args[1]
        network = args[2]

        component_from = network.get_component(host_from)
        component_to = network.get_component(host_to)

        if (component_to.get_name(),agent) in component_from.get_active_connections() and (component_from.get_name(),agent) in component_to.get_active_connections():
            component_from.remove_active_connection(component_to.get_name(), agent)
            component_to.remove_active_connection(component_from.get_name(), agent)
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
        host_name = args[0]
        network = args[1]
        component = network.get_component(host_name)

        if agent.get_name() == "attacker" and agent.get_priviledge_level() > component.get_highest_priviledge():

            active_accounts = component.get_active_accounts()
            agent.add_knowledge()
            return 1

        return 0

    except:
        return -1

# action: priviledge escalation on host X
# preconditions: agent is attacker and attacker has to have low-level priviledge on host X
# postconditions: priviledge level is increased by 1
def escalate_priviledges(agent, args):

    try:
        host_name = args[0]
        network = args[1]

        if agent.get_name() == "attacker" and agent.get_priviledge_level(host_name) != 0:
            agent.set_priviledge_level(self, host_name, agent.get_priviledge_level(host_name) + 1)
            return 1
        return 0
    except:
        return -1

# action: enumerate host X
# preconditions: agent is attacker and agent has escalated priviledges on host X, and agent did not already enumerated host X
# postconditions: agent has enumerated host X, agent knows all active connections of host X
def enumerate_host(agent, args):

    try:

        host_name = args[0]
        network = args[1]

        if agent.get_name == "attacker" and agent.get_priviledge_level(host_name) == host_name.get_highest_priviledge() \
            and host_name not in agent.enumerated():

            agent.add_enumerated(host_name)
            agent.add_knowledge("active_connections", host_name.get_active_connections())
            return 1

        return 0

    except:
        return -1

# action: exfiltrate data from host X
# preconditions: agent is attacker and agent has escalated priviledges on host X, enumerated host X and did not already exfiltrated host X
# postconditions: agent exfiltrated host X
def exfiltrate(agent, args):

    try:

        host_name = args[0]
        network = args[0]

        if agent.get_name == "attacker" and agent.get_priviledge_level(host_name) == host_name.get_highest_priviledge() and \

            agent.is_enumerated(host_name) and not agent.is_exfiltrated(host_name):
            agent.add_exfiltrated(host_name)
            print("Host {} exfiltrated".format(host_name))
            return 1

        return 0

    except:
        return -1


''' action template
# action: [name of the action]
# preconditions: [preconditions that needs to be satisfied to perform action]
# postconditions: [postconditions that happen once the action is successfully executed]
def action_name(agent, args):

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













