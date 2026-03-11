# Network Automation Lab — Project Notes

## Overview

This project is a Python-based network automation tool that connects to Cisco IOS routers and switches over SSH, retrieves their running configurations, and detects any changes by comparing against stored backups. The goal is to build a practical, real-world tool while learning core network automation concepts.

---

## Environment Setup

### Step 1: Create a Virtual Environment

The first step was isolating project dependencies by creating a Python virtual environment:

```bash
python3 -m venv network_automation_env
source network_automation_env/bin/activate
```

### Step 2: Install Dependencies

With the virtual environment active, the required library was installed:

```bash
pip install netmiko
```

Netmiko is a multi-vendor SSH library for network devices, built on top of Paramiko. It simplifies connecting to and sending commands to Cisco (and other vendor) devices.

---

## Choosing a Test Environment

### Mistake #1 — GNS3 on an Apple Silicon Mac

My initial plan was to use **GNS3** as a local network simulator. GNS3 lets you run virtual Cisco IOS images directly on your machine, which would have been ideal for isolated, offline testing.

**The problem:** GNS3 relies on running actual Cisco IOS images inside QEMU virtual machines. On an **M1/M2 Mac (Apple Silicon)**, QEMU's x86 emulation is either unsupported or too slow to be usable with Cisco IOS images. After spending time attempting to get it working, I concluded that GNS3 is not a viable option on Apple Silicon without significant workarounds.

**Lesson learned:** Always verify tool compatibility with your hardware architecture before committing to it. Apple Silicon (ARM) has notable compatibility gaps with legacy x86-based network emulation tools.

### Solution — Cisco DevNet Sandbox

I pivoted to using **Cisco DevNet Sandboxes**, which are free, cloud-hosted lab environments provided by Cisco. These require no local hardware and are accessible over the internet via SSH.

**Step:** Create a free Cisco DevNet account at developer.cisco.com.

---

## Selecting the Right DevNet Sandbox

Not all DevNet sandboxes provide the same level of access. This was another learning moment.

### Mistake #2 — Choosing a Restricted Sandbox

My first sandbox selection used a router that was locked to **privilege level 1**. At privilege level 1, you can only run a limited set of show commands and cannot enter global configuration mode (`conf t`). This severely limits what automation scripts can do.

![Restricted sandbox — privilege level 1](image.png)

*The router above only allowed read-only, unprivileged access.*

### Solution — Cisco IOS XE on DevNet

After consulting developer forums, I switched to the **Cisco IOS XE Always-On DevNet Sandbox**. This environment provides full privilege-level access, including the ability to enter enable mode and global configuration mode — which is required for meaningful automation.

![Cisco IOS XE DevNet Sandbox](image-1.png)

---

## Automation Logic

### Planned Workflow

The core script follows this sequence:

1. **Load inventory** — read the list of target devices from a YAML file
2. **Connect via SSH** — use Netmiko to establish an SSH session to each device
3. **Retrieve running config** — execute `show running-config` on the device
4. **Check for existing backup** — look for a previously saved configuration file
5. **Compare configs** — if a backup exists, diff it against the newly retrieved config
6. **Report changes** — surface any detected differences
7. **Save new backup** — store the latest config as a timestamped backup file

---

## Key Bugs & Lessons (Coding)

### Bug — `ConnectHandler(device)` vs `ConnectHandler(**device)`

When passing a device dictionary to Netmiko's `ConnectHandler`, the dictionary must be **unpacked** using `**`:

```python
# Wrong
connection = ConnectHandler(device)

# Correct
connection = ConnectHandler(**device)
```

Without `**`, Python passes the entire dictionary as a single positional argument rather than as keyword arguments, causing a `TypeError`.

### Bug — Extra Keys in the Device Dictionary

The device inventory YAML includes a `name` field (e.g. `"Router-1"`) for human-readable identification. However, Netmiko's `ConnectHandler` does not accept a `name` key and will raise an error if it is present.

The fix is to strip that key before passing the dictionary to Netmiko:

```python
device_params = {k: v for k, v in device.items() if k != "name"}
connection = ConnectHandler(**device_params)
```





---

## Connecting to the DevNet Sandbox via VPN (OpenConnect)

The reserved DevNet sandbox requires a VPN connection. This project uses **OpenConnect**, a free open-source alternative to Cisco AnyConnect.

### Step 1: Install OpenConnect

```bash
brew install openconnect
```

### Step 2: Connect to the VPN

```bash
sudo openconnect devnetsandbox-usw1-reservation.cisco.com:20260
# When prompted:
# Username: musaarsl
# Password: <your reservation password>
```

> Note: The VPN credentials are specific to each reservation and will change when you reserve a new sandbox.

### Step 3: Verify the connection

Ping a sandbox device to confirm connectivity:

```bash
ping 10.10.20.48
```

Then SSH in directly:

```bash
ssh developer@10.10.20.48
# Password: C1sco12345
```

### Important Notes

- Sandbox reservations have a time limit — extend it on the DevNet portal before it expires.
- If you see a certificate warning on first connect, accept it — this is normal for DevNet sandboxes.
