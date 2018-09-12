#!/usr/bin/env python 

import sys
import json
import os
import base64
import subprocess
import tempfile

output_location = sys.argv[1]
credential_string = os.environ["INPUT_credentials"]
subscription_id = os.environ["INPUT_subscription_id"]
credentials = json.loads(credential_string)
app_id = credentials["appId"]
password = credentials["password"]
tenant_id = credentials["tenant"]

def run_az(cmd, **kwargs):
    gcloud_cmd = ["az"]
    env = os.environ
    for k, v in kwargs.iteritems():
        env[k] = v
    print "Executing", " ".join(gcloud_cmd + cmd)
    return subprocess.Popen(gcloud_cmd + cmd, env=env)

print "Activating subscription", subscription_id
proc = run_az(["account", "set", "--subscription", subscription_id])
if proc.wait() != 0:
    sys.exit(1)

print "Activating service account"
proc = run_az(["login", "--service-principal", "-u", app_id, "-p", password, "--tenant", tenant_id])
if proc.wait() != 0:
    sys.exit(1)

result = {
    "client_id": credentials["appId"],
    "client_secret": credentials["password"],
    "tenant_id": credentials["tenant"],
    "subscription_id": subscription_id,
    "service_principal_name": credentials["name"],
}

for key, value in result.iteritems():
    print "Setting output", key

with open(output_location, 'w') as f:
    f.write(json.dumps(result))
