# HackFSU IDE Guide
Setup Guides for **[PyCharm](https://www.jetbrains.com/pycharm/)** and **[Webstorm](https://www.jetbrains.com/webstorm/)**. 

#### JetBrains Student License
JetBrains, the producers of PyCharm and Webstorm, offer free student licenses which are automatically approved with a `.edu` email. Create an account and apply for a student license before proceeding, as most of the features used in this guide rely on the *Professional* editions of the software. 

**Be sure to install the *Professional* editions of the software.**

## API Development with Pycharm

We recommend Pycharm not only as a powerful Python IDE, but also as a robust Docker Deployment UI.

#### Configure PyCharm with Docker
1. Create a run configuration via the top-right dropdown menu option "Edit Configurations".
    * Click the plus button in the top-right and select "Docker Deployment".
    * Select "Server" as your Docker Host (see **Docker Host Setup** in `.docker/README.md`).
    * Select "Deployment" as `docker-compose.yml` (see **Docker Compose Configs** above).
    * Check "Single Instance Only".
2. Add the Compose service as a remote project interpreter:
    * Open Preferences > Project: HackFSU > Project Interpreter
    * Click the options button next to the 'Project Interpreter' dropdown, select "Add Remote". 
    * Select "Docker Compose" from the radio buttons.
        * Choose your Docker host as the server (same as step 1).
        * Make sure it automatically selected your `docker-compose.yml` file.
        * Service should be "api", and interpreter should be "python". 
        
## Webapp Development with WebStorm
TODO