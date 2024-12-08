#!/bin/bash

# Add the NVIDIA Docker GPG key
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -

# Get the distribution information (Ubuntu version)
distribution=$(. /etc/os-release; echo $ID$VERSION_ID)

# Add the NVIDIA Docker repository
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# Update the package list
sudo apt-get update

# Install NVIDIA Docker 2
sudo apt-get install -y nvidia-docker2

# Restart Docker to apply changes
sudo pkill -SIGHUP dockerd

echo "NVIDIA Docker 2 installation completed successfully."
