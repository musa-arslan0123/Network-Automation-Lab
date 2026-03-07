#import the Netmiko connection class

#open a connection using the device dictionary

#enter enable mode if needed

#send show running-config

#store the output

#disconnect

#return the output



from netmiko import ConnectHandler



def get_running_config(device):
    
    
    connection = ConnectHandler(device)
    
