# Network Config Backup & Change Detection


Automated configuration management for Cisco IOS devices using Python. 

This project provides automated backup and change detection for Cisco IOS routers and switches. The tool establishes SSH connections to network devices, retrieves running configurations, stores versioned backups, and detects configuration drift over time.

The goal is to reduce manual CLI work, improve visibility into infrastructure changes, and maintain a reliable configuration history. By identifying unauthorised or unexpected modifications, the tool supports operational stability and strengthens network security.

## Core Functions

1. Detect configuration drift
2. Automatically back up configurations after validation



## Features

- SSH connection to Cisco IOS devices
- Running configuration retrieval
- Configuration comparison against previous backup
- Automated backup storage
- Local configuration archive
- Inventory-based device management

## Lab Environment

- macOS
- Python 3.9.6
- Netmiko for SSH-based device automation
- GNS3 for network simulation [may use cisco devnet sandbox to emulate and connect to devices]
- Cisco IOSv router with SSH enabled





