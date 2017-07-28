# Guide to installing server

## Installing dependencies

The server has several dependencies not usually installed on an operating system. See the repository at https://github.com/hackfsu/hackfsu_com#running-full-server.

This guide assumes you are using a unix-style system such as macOS or Ubuntu. If you're running Windows, good luck and consider a PR for this guide when you've figured it out.

### Preface: Ubuntu (or other Linux) only
You need to make sure your package manager is up to date before installing packages. Run an update on the available packages now. For example, on Ubuntu the command is:

```
sudo apt update
```

### Node.js

#### Install `nvm`, Node Version Manager

```
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.2/install.sh | bash
```

The script clones the nvm repository to ~/.nvm and adds the source line to your profile (~/.bash_profile, ~/.zshrc, ~/.profile, or ~/.bashrc).

Read more about it [here](https://github.com/creationix/nvm#installation).

#### Using `nvm` to install Node.js and `npm`.

```
nvm install 6
```

This will install the latest version of Node.js 6.x. **This will also install a copy of npm**.

#### Update npm

```
npm install -g npm
```

This will update npm to the latest version. You can check the version that gets install using `npm --version`. As of writing this, the node version is `5.0.3`. Make sure you have something newer than that.

#### Installing Node dependencies

This step can be done later, as it is required to build the site, but not for any of the setup steps. **This needs to be done before building the frontend.**

```
npm install
```

### Python

#### Package Managing

We recommend installing Python through a package manager. If you are using a Linux distro, you almost certainly have a package manager installed. For example, Ubuntu has `apt` install (which is a newer version of `apt-get`).

However, **if you are using macOS**, you will need to install a package manager. This guide recommends using **Homebrew**, although alternatives exists such as Macports.

##### Installing Homebrew (macOS only)

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

This command installs the homebrew package manager, which is executed in the terminal using the `brew` command. More information on Homebrew can be installed at [brew.sh](brew.sh).

#### Installing Python and Python3

Python has two major distributions, Python 2.x and Python 3.x. There are significant differences between them, and both are required by this project. Python 2.x is typically referenced as `python`, and Python 3.x typically is `python3`. We will now install both using the following commands:

##### For Ubuntu and other Linux systems
```
sudo apt install python
sudo apt install python3
```

##### For macOS
```
brew install python
brew install python3
```

Sometimes, certain versions of python may already be installed on your system. That's fine!

##### Addendum: installing `pip`
Sometimes, the python package manager known as `pip` will be installed alongside the versions of python. This is not always the case. For example, on Ubuntu you need to install it using:

```
sudo apt install python-pip
```

For other systems, please see your options [here](https://pip.pypa.io/en/stable/installing/).

**Make sure your pip version is newer than 3.5**.

##### Installing virtualenv and virtualenvwrapper
Virtualenv is a sandboxing tool which will allow you to install instances of Python libraries separate from the rest of your machine. Virtualenvwrapper is a tool which wraps virtualenv commands to make it easier to work with.

For local development, we strongly recommend installing virtualenvwrapper. For server deployment, do not use virtualenvwrapper. As this guide aims towards local development, we will be covering installing and using virtualenvwrapper. For non-wrapper deployment, please consult the repository's README.

You can install virtualenvwrapper with the following command: 

```
sudo pip install virtualenvwrapper
```

Then, add the following lines to your shell configuration file. In many instances, this will be your `.bashrc`, or `.bash_profile`.

```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
```

Then, close your terminal and open a new instance to finish initializing virtualenvwrapper. 

##### Installing python requirements

Once all other python requirements are satisfied create a virtualenv:
```
mkvirtualenv hackfsu -p <path/to/python3>
```

You can get the path to your python3 instance by using the command `which python`, and use the output as the path. In many cases, the output will be along the lines of `/usr/bin/python3`. 

With your virtualenv active, your shell should now be preceded by a `(hackfsu)`, assuming `hackfsu` is the name of your virtualenv. See the example below:

```
(hackfsu) andrew@macbook:~ $  
```

With your virtualenv activated, you now need to install the project's dependencies. Use the following command (this command assumes you are in the project's folder top-level folder).

```
pip install -r requirements.txt
```

## Conclusion

All of the project's required dependencies and libraries should now be installed. Please contact `andrewsosa` on Github if there is an issue with this guide.