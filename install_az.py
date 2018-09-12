#!/usr/bin/env python 

import sys
import os
import subprocess

def is_az_in_PATH():
    for directory in os.environ.get("PATH", "").split(":"):
        dest = os.path.join(directory, "az")
        if os.path.exists(dest):
            print "Found 'az' at", dest
            return True
    return False

def install_az():
    if is_az_in_PATH():
        return
    url = "https://aka.ms/InstallAzureCliBundled"
    print "Installing 'az'"
    lsb_release = subprocess.check_output(["lsb_release", "-cs"])
    deb = "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ " + lsb_release + " main" 
    with open("/etc/apt/sources.list.d/azure-cli.list") as f:
        f.write(deb)
    key = subprocess.check_output(["curl","-s", "-o", "microsoft.asc", "-L", "https://packages.microsoft.com/keys/microsoft.asc"])
    subprocess.check_output(["apt-key", "add", "microsoft.asc"])
    subprocess.check_output(["apt-get", "install", "apt-transport-https"])
    subprocess.check_output(["apt-get", "update"])
    subprocess.check_output(["apt-get", "install", "azure-cli"])


install_az()
