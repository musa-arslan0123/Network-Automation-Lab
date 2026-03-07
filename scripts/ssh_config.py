from netmiko import ConnectHandler


def get_running_config(device):
    
    #removing the name of the host from the dict for connection handler
    temp_device = device.copy()
    temp_device.pop("name")
    
    #establish connection with router
    connection = ConnectHandler(**temp_device)


    #esculate privleges to privledged exec mode 
    connection.enable()

    #retrieve running-config from router
    output = connection.send_command("show running-config")

    #disconnect from the connection 
    connection.disconnect()

    return output




