#!/bin/bash

# Update and install necessary tools
sudo apt-get update
sudo apt-get install -y python3-pip git

# Clone the GitHub repository
REPO_URL="https://github.com/kalyani-jaware/Project.git"
git clone $REPO_URL final_project

# Navigate to the project directory
cd mobilenet_project

# Install Python dependencies
pip3 install -r requirements.txt

# Set up the service account key for authentication (if needed inside the app)
export GOOGLE_APPLICATION_CREDENTIALS="/lab-5-437901-4cd443d66c01.json"

# Copy the service account key (pre-uploaded to VM metadata)
if [ -f "/tmp/lab-5-437901-4cd443d66c01.json" ]; then
    sudo mv /tmp/slab-5-437901-4cd443d66c01.json /etc/lab-5-437901-4cd443d66c01.json
    sudo chmod 600 /etc/lab-5-437901-4cd443d66c01.json
fi

# Run the Streamlit app
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
