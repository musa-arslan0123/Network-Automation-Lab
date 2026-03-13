import yaml
import os

from scripts.ssh_config import get_running_config
from scripts.backup_manager import save_backup
from scripts.check_config import check_config



def main():

    with open("inventory/devices.yaml", "r") as f:
        devices = yaml.safe_load(f)

    devices = devices["devices"]

    for device in devices:

        new_config = get_running_config(device)

        backup_files = sorted([f for f in os.listdir("backups") if f.startswith(device["name"])])

        if backup_files:
            latest_backup = "backups/" + backup_files[-1]
            with open(latest_backup, "r") as f:
                old_config = f.read()
            check_config(old_config, new_config)

        save_backup(device["name"], new_config)

if __name__ == "__main__":
    main()

    