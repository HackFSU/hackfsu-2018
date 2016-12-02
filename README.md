HackFSU Website
===============

Remake of previous node version for 2017, now written in Django.

# Contributing
## Development Requirements
### Running front-end demo
* nodejs 6.x

Run the demo. Does not access real server, just a mock express one.
```bash
$ npm install
$ npm run demo
```


### Running full server
* a copy of `./hackfsu_com/secret_keys.json` (get from someone)
* python3.5
* pip3.5
* virtualenv
* nodejs 6.x

Setup virtualenv (do once)
```bash
$ virtualenv -p /path/to/python3.5 /path/to/repo/venv
```

Update virtualenv (do every time requirements changes)
```bash
$ ./venv/bin/pip3.5 install -r requirements.txt
```

Build frontend with npm
```bash
$ npm intall
$ npm run build
```

Run server in virtualenv
```bash
$ ./venv/bin/python manage.py runserver 8000

```

Make these tasks easier by using PyCharm and setting up run commands.


# Server deployment
Push an update to live, then run a deploy. Server access required.

The deploy script makes updating the server easy. This assumes it has already
been setup on the server. See Jared for server setup guide.
```
$ git push origin master
$ git push origin master:live
$ ssh hackfsu.com
[hackfsu]$ sudo /root/deploy.sh
```