#!/usr/bin/env bash

# Install packages needed wit Apt
sudo apt update
sudo apt install -y python3 python3-pip virtualenv nginx

# Setup python virtualenv
cd /home/www/minecraft_user_logger/
sudo virtualenv -p python3 venv
source venv/bin/activate

# Install pip dependencies
sudo pip3 install -r requirements.txt

# Start nginx:
sudo systemctl start nginx

# Configure nginx
sudo rm /etc/nginx/sites-enabled/default
sudo touch /etc/nginx/sites-available/minecraft_user_logger
sudo ln -s /etc/nginx/sites-available/minecraft_user_logger /etc/nginx/sites-enabled/minecraft_user_logger

sudo echo -e "server {\n    location / {\n        proxy_pass http://localhost:8000;\n        proxy_set_header Host $host;\n        proxy_set_header X-Real-IP $remote_addr;\n    }\n    location /static {\n        alias  /home/www/minecraft_user_logger/src/static/;\n    }\n}" > /etc/nginx/sites-enabled/minecraft_user_logger

sudo systemctl restart nginx