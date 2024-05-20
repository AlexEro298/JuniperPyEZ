#import libary
import datetime, time, os
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError

#1 authorization method
#2 authorization method
import authentification

#passed arguments for console (1 authorization method)
#script_name, username, password, host = argv
#or (2 authorization method)
username = authentification.username
password = authentification.password
hosts = authentification.ip_device

#File rotation
def file_rotation(days, path):
    now = time.time()
    file_compare = now - days * 86400
    for filename in os.listdir(path):
        file_stamp = os.stat(os.path.join(path, filename)).st_mtime
        if file_stamp < file_compare:
            os.remove(os.path.join(path, filename))

#начало программы
if __name__ == "__main__":

    # current date and time
    now_date = datetime.datetime.now().strftime("%Y%m%d")
    now_time = datetime.datetime.now().strftime("%H:%M:%S").replace(':', '.')
    path_log = '/samba/log/save_config'
    #rotation days
    days = 30

    #rotation log
    file_rotation(days, f'{path_log}')

    file_log = open(f'{path_log}/save_config_{now_date}_{now_time}.txt', 'w')

    for host in hosts:
        #saving path
        path = f'/samba/hosts/{host}'
        path_set=f'{path}/set'

        #rotation config
        file_rotation(days, f'{path}')
        file_rotation(days,f'{path_set}')


        try:
            # connect device
            dev = Device(host=host, user=username, password=password, gather_facts=False)
            dev.open()
            file_log.write(f'Connect to {host}, OK!\n')

        except ConnectError as err:
            file_log.write(f'Can\'t connect to device. {err} \n')
            continue

        # current_config
        current_config = dev.cli('show configuration | display omit')
        file_current_config = open(f'{path}/current_config_{now_date}_{now_time}_{host}.txt', 'w')
        file_current_config.write(current_config)
        file_current_config.close()

        # current_config_set
        current_config_set = dev.cli('show configuration | display set')
        file_current_config_set = open(f'{path_set}/current_config_set_{now_date}_{now_time}_{host}.txt', 'w')
        file_current_config_set.write(current_config_set)
        file_current_config_set.close()

        # disconnect device
        dev.close()

    #close log
    file_log.close()