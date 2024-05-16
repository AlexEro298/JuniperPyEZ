# To use this project, need:

1. Use command:
* git clone https://github.com/AlexEro298/JuniperPyEZ
* cd JuniperPyEZ
* python -m venv ./venv
* . venv/bin/activate;
* pip install -r requirements.txt
* python save_config.py
* deactivate;

2. Create a file with the name: 
* authentification.py

3. In the file write:
* username = ''
* password = ''
* ip_device = ['', '']

4. Use cron:
* crontab -l - task cron
* crontab -e - add cron
* nano /var/spool/cron/root - manual add cron
* 0 * * * * /samba/scriptsPython/JuniperPyEZ/bash_script - every hour