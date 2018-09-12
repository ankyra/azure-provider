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
    print "Downloading bundle from", url
    subprocess.check_output(["curl","-s", "-o", "azure-cli_bundle.tar.gz", "-L", url])
    print "Unpacking bundle"
    subprocess.check_output(["tar", "-xvzf", "azure-cli_bundle.tar.gz"])
    print "Running the installer"
    if subprocess.Popen(["bash", "azure-cli_bundle_*/installer"]).wait() != 0:
        sys.exit(1)

install_az()
