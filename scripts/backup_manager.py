import datetime as dt


def save_backup(device_name, config):

    date_stamp = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    complete_stamp = device_name + "_" + date_stamp

    path = 'backups/' + complete_stamp + ".txt"
    
    with open(path, "w") as f:
        f.write(config)


