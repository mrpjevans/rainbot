# rainbot
Python script to control the MagPi Rain Detector project. See
raspberypi.org/magi issue #74 for more details.

## Pre-requisites
Make sure gpiozero is installed.

```bash
sudo apt install python3-gpiozero
```

## Installation

#### From git

```bash
cd
git clone https://github.com/mrpjevans/rainbot.git
```

#### Manually

```bash
mkdir ~/rainbot
cd rainbot
nano rainbot.py
```

Now cut and paste (or manually enter) the code.

## Running

```python
cd ~/rainbot
python3 rainbot.py
```

## Run At Startup

Create the following file as a superuser:

```bash
sudo nano /lib/systemd/system/rainbot.service
```

Add in the following text:

```
[Unit]
Description=Rainbot           
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 /home/pi/rainbot/rainbot.py

[Install]
WantedBy=multi-user.target
```

Ctrl+X to save and quit out of nano. Now issue the following command:

```bash
sudo chmod 644 /lib/systemd/system/klaxon.service
sudo systemctl daemon-reload
sudo systemctl enable klaxon.service
```

The script will now start in the background on reboot.
