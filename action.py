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
        return -1
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
        return -1
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
        return -1
    except:
        return -1












