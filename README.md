# minecraft_user_logger

### Requirements
* git
* python3
* python3-pip
* virtualenv
* nginx

##### On Ubuntu 16.04
```
sudo apt update
sudo apt install -y git python3 python3-pip virtualenv nginx
```

### Setup environment
Create new directory to store project:
```
sudo mkdir /home/www && /home/www
```

Clone git repository
```
sudo git clone https://github.com/NationCraft/minecraft_user_logger.git
```

Create and activate virtualenv:
```
cd minecraft_user_logger/
sudo virtualenv -p python3 venv
source venv/bin/activate
```

Install Python dependencies:
```
sudo pip3 install -r requirements.txt
```

### Configure nginx
Start nginx:
```
sudo systemctl start nginx
```

Then:
```
sudo rm /etc/nginx/sites-enabled/default
sudo touch /etc/nginx/sites-available/minecraft_user_logger
sudo ln -s /etc/nginx/sites-available/minecraft_user_logger /etc/nginx/sites-enabled/minecraft_user_logger
```

Make config file for minecraft_user_logger:
```
sudo vim /etc/nginx/sites-enabled/minecraft_user_logger
```
Add:
```
server {
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /static {
        alias  /home/www/minecraft_user_logger/src/static/;
    }
}

```

Restart nginx:
```
sudo systemctl restart nginx
```

Test:
```
cd /home/www/minecraft_user_logger/
gunicorn run:app -b localhost:8000
```