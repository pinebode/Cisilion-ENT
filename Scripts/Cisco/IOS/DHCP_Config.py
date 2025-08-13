# This script was created to generate DHCP related configuration scripts

dhcp_pool_template = [
    "network",
    "domain-name",
    "default-router",
    "dns-server",
    "lease"]

dhcp_host_template = [
    "host",
    "hardware-address",
    "default-router",
    "dns-server",
    "lease"]

dhcp_exclude = "ip dhcp excluded-address"
remove_help_addr = ["interface vlan", "no ip helper-address"]


def pool_generator(name, domain, net, gateway, dns, lease='8'):
    '''This is a dhcp network config generator. It takes input from the user and puts it in the correct fields
    and returns the result.'''
    net_config = []
    net_config.append(f"ip dhcp pool {name}")
    for cmd in dhcp_pool_template:
        if "net" in cmd:
            net_config.append(f"{cmd} {net}")
        elif 'domain' in cmd:
            net_config.append(f"{cmd} {domain}")
        elif 'router' in cmd:
            net_config.append(f"{cmd} {gateway}")
        elif 'dns' in cmd:
            net_config.append(f"{cmd} {dns}")
        else:
            net_config.append(f"{cmd} {lease}")

    net_config.append('!')
    return net_config


def host_generator(name, host, client_ID, gateway, dns, lease='8'):
    """This is a dhcp reservation config generator. It takes input from the user, populates the fields in the
    config and returns the config output in a list."""
    host_config = []
    host_config.append(f"ip dhcp pool {name}")
    for cmd in dhcp_host_template:
        if "host" in cmd:
            host_config.append(f"{cmd} {host}")
        elif 'client' in cmd or 'hardware' in cmd:
            host_config.append(f"{cmd} {client_ID}")
        elif 'router' in cmd:
            host_config.append(f"{cmd} {gateway}")
        elif 'dns' in cmd:
            host_config.append(f"{cmd} {dns}")
        else:
            host_config.append(f"{cmd} {lease}")

    host_config.append('!')
    return host_config


def mac_generator(mac):
    """A quick function to reformat mac addresses so that its in the format that cisco devices accept"""
    mac_format = '{}{}.{}{}.{}{}'
    if '.' in mac:
        return mac
    elif '-' in mac:
        mac_gen = mac.split('-')
        return mac_format.format(mac_gen[0], mac_gen[1], mac_gen[2], mac_gen[3], mac_gen[4], mac_gen[5])
    elif ':' in mac:
        mac_gen = mac.split(':')
        return mac_format.format(mac_gen[0], mac_gen[1], mac_gen[2], mac_gen[3], mac_gen[4], mac_gen[5])
    else:
        return "Sorry i don't recognize that, try again"
    

def client_mac_generator(mac):
    """A quick function to reformat mac addresses so that its in the client-id format that cisco devices accept"""
    client_format = '01{}.{}{}.{}{}.{}'
    if '.' in mac:
        mac_gen = mac.split('.')
        return client_format.format(mac_gen[0], mac_gen[1], mac_gen[2], mac_gen[3], mac_gen[4], mac_gen[5])
    elif '-' in mac:
        mac_gen = mac.split('-')
        return client_format.format(mac_gen[0], mac_gen[1], mac_gen[2], mac_gen[3], mac_gen[4], mac_gen[5])
    elif ':' in mac:
        mac_gen = mac.split(':')
        return client_format.format(mac_gen[0], mac_gen[1], mac_gen[2], mac_gen[3], mac_gen[4], mac_gen[5])
    else:
        return "Sorry i don't recognize that, try again"

'''
Simple tshoot test to ensure functions work
maca = mac_generator(input("Please enter a mac address: "))
macab = client_mac_generator(input("Please enter a mac address: "))
print(maca)
print(macab)
'''

domain = input("Next, enter the domain-name: ")
dhcp_configs = []
host_configs = []
while True:
    question = input("\nSelect one, DHCP pool or HOST pool?(type 'q' to quit) ").lower()
    if question == 'dhcp' or question == 'host':
        if 'dhcp' in question:
            dhcp = input("Please enter the name of your DHCP pool: ")
            network = input("Now enter the network address (for e.g. 10.1.1.0 /24): ")
            gw = input("Next, enter the default-gateway: ")
            dns = input("Finally, enter your dns servers (separated by a space for e.g. 8.8.8.8 4.4.2.2): ")
            prompt = input("Lease default is 8 days, would you like to change (y or n)? ")
            if prompt == 'y':
                new_lease = input("set the lease in the format 'days hours mins' (for e.g. 8 hours is 0 8): ")
                dhcp_configs.append(pool_generator(dhcp, domain, network, gw, dns, lease=new_lease))
            elif prompt == 'n':
                dhcp_configs.append(pool_generator(dhcp, domain, network, gw, dns))
        elif 'host' in question:
            hostname = input("Please enter the name of your HOST pool: ")
            host = input("Now enter the host address (for e.g. 10.1.1.10 255.255.255.0): ")
            mac_question = input("Do you require a client-id or hardware address? ").lower()
            if 'client' in mac_question:
                dhcp_host_template[1] = 'client-identifier'
                client_id = input("Enter the MAC address of the host (e.g. abcd.1234.5678): ")
                mac_address = client_mac_generator(client_id)
            elif 'hardware' in mac_question:
                dhcp_host_template[1] = 'hardware-address'           
                hardware_id = input("Enter the MAC address of the host (e.g. abcd.1234.5678): ")
                mac_address = mac_generator(hardware_id)
            gw = input("Next, enter the default-gateway: ")
            dns = input("Finally, enter your dns servers (separated by a space for e.g. 8.8.8.8 4.4.2.2): ")
            prompt = input("Lease default is 8 days, would you like to change (y or n)? ")
            if prompt == 'y':
                new_lease = input("set the lease in the format 'days hours mins' (for e.g. 8 hours is 0 8): ")
                host_configs.append(host_generator(hostname, host, mac_address, gw, dns, lease=new_lease))
            elif prompt == 'n':
                host_configs.append(host_generator(hostname, host, mac_address, gw, dns))

    elif question == 'q':
        break
    else:
        print("Sorry wrong value entered. Try Again.")
        question = input("\nSelect one, DHCP pool or HOST pool?(type 'q' to quit) ").lower()
        if question == 'q':
            break
        else:
            continue


'''
Simple Test to ensure script is working so far as expected
print(dhcp_configs)
print(host_configs)
'''

exclude_list = []
while True:
    question2 = input("\nWould you like to exclude any dhcp addresses, y or n? ")
    if question2 == 'y':
        user = input("Please enter your address range to exclude separated by a space (e.g. 10.1.1.250 10.1.1.254: ")
        exclude_list.append(user)
    else:
        break

helper_addresses = []
while True:
    question3 = input("\nWould you like to remove any helper-addresses, y or n? ")
    if question3 == 'y':
        vlan = input("Please enter the VLAN interface number: ")
        helpers = input("Please enter the ip helper addresses. (Separate each with a space if more than 1): ")
        cmd1, cmd2 = remove_help_addr
        temp_list = []
        temp_list.append(f"{cmd1} {vlan}")
        temp_list.append(f"{cmd2} {helpers}")
        helper_addresses.append(temp_list)
    else:
        break

file = input("Please give a name for the file where your config will be stored: ")
with open(file, 'w') as f:
    for item in dhcp_configs:
        for line in item:
            if 'pool' in line:
                f.write(f'{line}\n')
            elif line == '!':
                f.write(line+'\n')
            else:
                f.write(f" {line}\n")

    for item in host_configs:
        for line in item:
            if 'pool' in line:
                f.write(f'{line}\n')
            elif line == '!':
                f.write(line+'\n')
            else:
                f.write(f" {line}\n")

    if exclude_list:
        for item in exclude_list:
            f.write(f"{dhcp_exclude} {item}\n")
        else:
            f.write('!\n')

    if helper_addresses:
        for item in helper_addresses:
            f.write(f"{item[0]}\n {item[1]}\n")
        else:
            f.write('!\n')
