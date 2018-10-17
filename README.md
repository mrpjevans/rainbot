[README.md in Simplified Chinese in Github](https://github.com/TommyZihao/MagPi_Chinese/blob/master/MagPi74_46-49%E7%94%A8%E6%A0%91%E8%8E%93%E6%B4%BE%E5%81%9A%E4%B8%8B%E9%9B%A8%E8%AD%A6%E6%8A%A5%E5%99%A8.md)

[README.md in Simplified Chinese faster link in China](https://blog.csdn.net/qq_41822781/article/details/83119439)
# rainbot
Python script to control the MagPi Rain Detector project. See
raspberypi.org/magpi issue #74 for more details.

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

Ctrl+X to save and quit out of nano. Now issue the following commands:

```bash
sudo chmod 644 /lib/systemd/system/rainbot.service
sudo systemctl enable rainbot.service
sudo systemctl daemon-reload
```

The script will now start in the background on reboot.
