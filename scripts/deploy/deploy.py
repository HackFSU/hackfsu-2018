import os
import paramiko
import getpass
import simplecrypt
import pickle

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


def deploy():
    if not load_cache():
        prompt_input()
        save_cache()
    else:
        print('Using config cache ' + CONFIG_CACHE_FILE)

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(CONFIG['host'], username=CONFIG['host_username'], password=CONFIG['host_password'])

    cmd = 'sudo /bin/bash ' + CONFIG['deploy_script_path']

    print(CONFIG['host_username'] + '@' + CONFIG['host'] + '# ' + cmd)

    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)

    stdin.write(CONFIG['host_sudo_password'] + '\n')
    stdin.write(CONFIG['github_username'] + '\n')
    stdin.write(CONFIG['github_password'] + '\n')
    stdin.flush()

    for line in stdout.read().splitlines():
        line = line.decode('utf-8')
        print(line)
    for line in stderr.read().splitlines():
        line = line.decode('utf-8')
        print('ERROR: ' + line)


if __name__ == '__main__':
    deploy()
