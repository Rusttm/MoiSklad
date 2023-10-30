# MoiSklad

1. Create venv: 
   # python3 -m venv bot_env
   # source bot_env/bin/activate
   # cd telegrambot/MoiSklad
   # pip install -r requirements.txt 

2. Create bash script:
#sudo nano /home/user/telegrambot/MoiSklad/TeleBotSerman.sh 

    #!/bin/bash
    # cd /telegrambot/MoiSklad
    /home/user/bot_env/bin/python /home/user/telegrambot/MoiSklad/TeleBotSerman.py >> /home/user/telegrambot/MoiSklad/logs/myapp.log 2>&1 

3. Create service for autorun
   # sudo nano /etc/systemd/system/telebot.service 

   [Unit]
   Description=TeleBotSerman 
   
   [Service]
   Type=simple
   WorkingDirectory=/home/rusttm/PycharmProjects/SermanBot/MoiSklad
   ExecStart=/home/rusttm/telegrambot/MoiSklad/TeleBotSerman.sh
   Restart=always
   User=rusttm 
   
   [Install]
   WantedBy=multi-user.target