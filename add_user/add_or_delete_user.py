import datetime
from jnpr.junos.utils.config import Config
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError

#authorization method
import authentification_user_edit

username = authentification_user_edit.username
password = authentification_user_edit.password
hosts = authentification_user_edit.ip_device

now_date = datetime.datetime.now().strftime("%Y%m%d")
now_time = datetime.datetime.now().strftime("%H:%M:%S").replace(':', '.')
#path_log = '/samba/log/add_user'

#add or delete user
action = 'dd'
#name user
add_user = 'test20'
#class user (default: super-user, read-only, operator)
add_user_class = 'super-user'
#full name user
add_user_full_name = 'test test'
#ssh (default: ssh-dsa, ssh-ecdsa, ssh-ed25519, ssh-rsa)
add_user_authentication = 'ssh-ed25519'
#public ssh-key
add_user_ssh_key = ''

#If need commit config use 'commit'
commit='commit'

#Entry point
if __name__ == "__main__":
    #file_log = open(f'{path_log}/add_user_{now_date}_{now_time}.txt', 'w')
    for host in hosts:
        try:
            #connect device
            dev = Device(host=host, user=username, password=password, gather_facts=False)
            dev.open()
            #file_log.write(f'Connect to {host}, OK!\n')
        except ConnectError as err:
            #file_log.write(f'Can\'t connect to device. {err} \n')
            continue

        #mode use edit configuration
        cu = Config(dev, mode='exclusive')

        try:
            cu.lock()
            # file_log.write(f'Lock configuration {host}, OK!\n')
            print('Open configuration')
        except Exception as err:
            # file_log.write(f'Сonfiguration cannot be opened {host}. {err}\n')
            print(err)
            continue

        if action == 'add':
            cu.load(f'set system login user {add_user} class {add_user_class} full-name \"{add_user_full_name}\" authentication {add_user_authentication} \"{add_user_ssh_key}\"',
            format='set')
        elif action == 'delete':
            cu.load(
                f'delete system login user {add_user}',
                format='set')
        else:
            print('Action is not specified')
            # file_log.write('Action is not specified')

        compare_config = cu.diff()
        #file_log.write(compare_config)
        print(f'Compare config: {compare_config}')

        try:
            check = cu.commit_check()
            # file_log.write(f'Check commit succes: {check}\n')
            print(f'Check commit succes: {check}\n')
        except Exception as err:
            # file_log.write(f'Сonfiguration cannot be commit {host}. {err}\n')
            print(f'Сonfiguration cannot be check commit {host}.\nCommit check: {err}\n')
            dev.close()
            continue

        if compare_config != None:
            if commit == 'commit':
                try:
                    print('commit config')
                    # file_log.write(f'Commit config\n')
                    cu.commit(comment=f'\"add new user {add_user}\"')
                except Exception as err:
                    # file_log.write(f'Сonfiguration cannot be commit {host}. {err}\n')
                    print(f'Сonfiguration cannot be commit {host}.\nCommit: {err}\n')
                    dev.close()
                    continue

        cu.unlock()
        dev.close()