#!/bin/bash

# Update and install necessary tools
sudo apt-get update
sudo apt-get install -y python3-pip git

# Clone the GitHub repository
REPO_URL="https://github.com/your-username/your-repo-name.git"
git clone $REPO_URL final_project

# Navigate to the project directory
cd mobilenet_project

# Install Python dependencies
pip3 install -r requirements.txt

# Set up the service account key for authentication (if needed inside the app)
export GOOGLE_APPLICATION_CREDENTIALS="/etc/service-account-key.json"

# Copy the service account key (pre-uploaded to VM metadata)
if [ -f "/tmp/service-account-key.json" ]; then
    sudo mv /tmp/service-account-key.json /etc/service-account-key.json
    sudo chmod 600 /etc/service-account-key.json
fi

# Run the Streamlit app
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
