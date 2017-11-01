# HackFSU Docker Guide

### Installing Docker

In our experience, we've found Windows, macOS, and Linux each work best with a different flavor of Docker:

1. Windows : [Docker Toolbox](https://docs.docker.com/toolbox/toolbox_install_windows/)<sup>1</sup>
2. macOS : [Docker for Mac](https://docs.docker.com/docker-for-mac/install/)
3. Linux: [Docker Community Edition](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/)<sup>2</sup>

<sup>1</sup>While Docker Toolbox is what our developers have managed to get working, we recommend using [Docker for Windows](https://docs.docker.com/docker-for-windows/) if possible.

<sup>2</sup>This links to the Ubuntu distribution, but other Linux distributions are available in the sidebar.

### Setting up your Docker Host
On macOS and Linux systems, by default your physical machine acts as the host for the Docker Containers. However, this is not the case with Windows. 

On Windows systems, you need to use the Docker Machine tool to provision a virtual machine via Virtualbox to act as your machine host. 

When Docker Toolbox installs, it should have automatically provisioned a Virtualbox VM to serve as the Docker host. This is what the "Quickstart Terminal" connects to to run commands. You can confirm whether or not this is true by running `docker-machine ls` in your command prompt, *not* the quickstart terminal. 

If you already have the Docker Machine Virtual Host created, you can activate it using the `docker-compose env` command. 


### Compose Configurations
See `/.docker/README.md`.