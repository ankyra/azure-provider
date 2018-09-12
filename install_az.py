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
    bundle_dir = None
    for fp in os.listdir("."):
        if fp.startswith("azure-cli_bundle_"):
            bundle_dir = fp
    if bundle_dir is None:
        print "Could not find the unpackaged bundle in its expected destination."
        sys.exit(1)
    installer_path = os.path.join(bundle_dir, "installer")
    print "Running the installer",  installer_path
    subprocess.check_output([installer_path])

install_az()
