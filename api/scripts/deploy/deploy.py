"""
    An attempt to make an auto-deploy that logs in via ssh and then runs the deploy.sh.

    Does not fully work, could not get the git creds to inject. Just log in and run the deploy.sh manually for now.
"""


import os
import paramiko
import getpass
import simplecrypt
import pickle
import signal
import sys

CONFIG_CACHE_FILE = os.path.dirname(os.path.abspath(__file__)) + '/config_cache.tmp'
CONFIG_CACHE_SECRET = 'secret'
CONFIG = {
    'host': '138.197.21.234',
    'host_username': '',
    'host_password': '',
    'host_sudo_password': '',
    'github_username': '',
    'github_password': '',
    'deploy_script_path': '/var/www/hackfsu_com/scripts/deploy/deploy.sh'
}

def prompt_input():
    """ Prompts for input """
    CONFIG['host_username'] = input(CONFIG['host'] + " username: ")
    CONFIG['host_password'] = getpass.getpass(CONFIG['host_username'] + "@" + CONFIG['host'] + " password: ")
    CONFIG['host_sudo_password'] = getpass.getpass(
        CONFIG['host_username'] + "@" + CONFIG['host'] + " sudo password <leave blank if same>: "
    )

    if len(CONFIG['host_sudo_password']) == 0:
        CONFIG['host_sudo_password'] = CONFIG['host_password']

    print()

    CONFIG['github_username'] = input("Enter GitHub username: ")
    CONFIG['github_password'] = getpass.getpass(CONFIG['github_username'] + "@github.com password: ")

    print()


def config(key):
    if len(CONFIG[key]) == 0:
        CONFIG[key] = getpass.getpass('Enter "'+key+'": ')
    return CONFIG[key]

def print_safe_config():
    """ Prints non-password config data """
    safe_keys = [
        'host',
        'host_username',
        'github_username',
        'deploy_script_path'
    ]
    for key in safe_keys:
        print('{} = "{}"'.format(key, CONFIG[key]))


def load_cache():
    print('Checking for config cache file ' + CONFIG_CACHE_FILE)

    if not os.path.isfile(CONFIG_CACHE_FILE):
        return False

    print('Config cache found. Loading...')

    # Load it into the config
    with open(CONFIG_CACHE_FILE, 'rb') as file:
        data = file.read()
        file.close()
        data = simplecrypt.decrypt(CONFIG_CACHE_SECRET, data)
        CONFIG.update(pickle.loads(data))

    return True


def save_cache():
    # Get encrypted pickle string
    data = simplecrypt.encrypt(CONFIG_CACHE_SECRET, pickle.dumps(CONFIG))

    # Save it to cache
    with open(CONFIG_CACHE_FILE, 'wb') as file:
        file.write(data)
        file.close()

    print('New config cache file created ' + CONFIG_CACHE_FILE)


def build_input():
    input_lines = [
        config('host_sudo_password'),
        config('github_username'),
        config('github_password')
    ]

    return 'echo -e "' + '\\n'.join(str(line).replace('"', '\"') for line in input_lines) + '\\n"'


def deploy():
    if not load_cache():
        prompt_input()
        save_cache()
    else:
        print('Using config cache ' + CONFIG_CACHE_FILE)

    print_safe_config()

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(config('host'), username=config('host_username'), password=config('host_password'))

    cmd = 'sudo -S /bin/bash ' + config('deploy_script_path')

    print('\n[{}@{}]# {}\n'.format(config('host_username'), config('host'), cmd))

    cmd = build_input() + ' | ' + cmd
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)

    def print_lines(prefix, lines):
        print()
        for line in lines:
            line = line.decode('utf-8')
            print(prefix + line)

    def stop(reason, output):
        ssh.close()
        print('\n--- Remote host closed (' + reason + ') ---')
        sys.exit(output)

    def kill_handler(signal, frame):
        print_lines('REMOTE STDOUT: ', stdout.read().splitlines())
        print_lines('REMOTE STDERR: ', stderr.read().splitlines())
        stop('SIGINT', 1)

    # Allow the results of the command to be printed before process exits with an interrupt
    signal.signal(signal.SIGINT, kill_handler)

    # Continuously grab output
    for stdout_line in iter(lambda: stdout.readline(2048), ""):
        print(stdout_line, end="")

    error_lines = stderr.read().splitlines()
    if len(error_lines) != 0:
        # An error has occurred somewhere
        print_lines('REMOTE STDERR: ', error_lines)
        stop('remote error', 1)
    else:
        stop('successful completion', 0)

if __name__ == '__main__':
    deploy()
