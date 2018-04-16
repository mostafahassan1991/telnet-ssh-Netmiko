from sys import argv
import csv
import getpass
from netmiko import ConnectHandler

script, csv_file = argv

reader = csv.DictReader(open(csv_file, 'rb'))

device_list = []

for line in reader:
    device_list.append(line)


username = raw_input("Username? ")
password = getpass.getpass("Password? ")
enablepw = getpass.getpass("Enable Password? ")

for device in device_list:
    print "\n\n----------------\nDevice: {0} \n---------------\n".format(device['host'])
    try:
        # we need to set the various options Netmiko is expecting.
        # We use the variables we got from the user earlier
        device['device_type'] = 'cisco_ios_ssh'
        device['username'] = username
        device['password'] = password
        device['secret'] = enablepw
        net_connect = ConnectHandler(**device)
        print "connected via ssh"

    except:

        try:
            # same as before, but using the 'telnet' device type
            device['device_type'] = 'cisco_ios_telnet'
            device['username'] = username
            device['password'] = password
            device['secret'] = enablepw
            net_connect = ConnectHandler(**device)
            print "connected via telnet"
        except:
            # this is the catch all except, if NOTHING works, tell the user and
            #  continue onto the next item in the for loop.
            print "Unable to connect!"

            continue
    # breaking out of the "try" block,
    # we now want to take the session into "enable mode" if it is not already
    net_connect.enable()
    # just printing a blank line. I like formatting the output neatly.
    print "\n"
    # Now to run a command and do checks on the output.
    output1 = net_connect.send_command("show ip int br")
    print output1
    print "====================="
    output2 = net_connect.send_command("show version | in Version")
    print output2



