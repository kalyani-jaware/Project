from googleapiclient import discovery
from google.auth import default
import os

# Configuration
PROJECT = "lab-5-437901"  # Replace with your GCP project ID
ZONE = "us-west1-b"  # Replace with your desired zone
INSTANCE_NAME = "final-project"
MACHINE_TYPE = "e2-medium"
IMAGE_PROJECT = "debian-cloud"
IMAGE_FAMILY = "debian-11"
STARTUP_SCRIPT_PATH = "startup-script.sh"

def create_vm():
    """Create a Google Cloud VM instance."""
    credentials, _ = default()
    compute = discovery.build("compute", "v1", credentials=credentials)

    # VM configuration
    config = {
        "name": INSTANCE_NAME,
        "machineType": f"zones/{ZONE}/machineTypes/{MACHINE_TYPE}",
        "disks": [
            {
                "boot": True,
                "autoDelete": True,
                "initializeParams": {
                    "sourceImage": f"projects/{IMAGE_PROJECT}/global/images/family/{IMAGE_FAMILY}",
                    "diskSizeGb": "50",
                },
            }
        ],
        "networkInterfaces": [
            {
                "network": "global/networks/default",
                "accessConfigs": [{"type": "ONE_TO_ONE_NAT", "name": "External NAT"}],
            }
        ],
        "metadata": {
            "items": [
                {"key": "startup-script", "value": open(STARTUP_SCRIPT_PATH, "r").read()},
                {"key": "enable-oslogin", "value": "TRUE"},
            ]
        },
        "tags": {"items": ["http-server", "https-server"]},
    }

    # Create the VM
    request = compute.instances().insert(project=PROJECT, zone=ZONE, body=config)
    response = request.execute()
    print(f"VM {INSTANCE_NAME} created successfully!")
    return response

def main():
    # Step 1: Create the VM
    create_vm()

if __name__ == "__main__":
    main()
