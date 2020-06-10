# Jackcast
Jackcast is a device used to stream/cast line-in (auxiliary input) audio to a
wireless device. Use this device to cast audio from a record player or other
old sound systems. 

This software is intended to run on a computer like a Raspberry Pi that can be
permanently connected to the audio device. Jackcast includes a webapp to control the
wireless device such as the volume and which device to stream too. Jackcast has
no concept or control of where the line-in audio is coming from which is why
there are no controls to play, pause and change the track.

Initial motivation [video](https://youtu.be/4KiZJvDQa0I) and demo.

This project is stable but a work in progress.

![Jackcast browser](https://github.com/wil3/jackcast/blob/master/.github/images/app-desktop.png)

## Supported Devices
* Sonos
* Chromecast (future: PRs welcome)
* Bluetooth (future: PRs welcome)

## Installation
The plan is to eventually host an image users can write to their SD card. In
the meantime you can manually install it. Some of the tasks have been automated
but a number are still manual. The following assume you don't have
an extra keyboard/mouse/monitor. It may be easier to setup if you have these
devices. Please report any issues with these instructions.

* Use the [Raspberry Pi
  Imager](https://www.raspberrypi.org/documentation/installation/installing-images/)
to install Ubuntu Server 20.04
* [Enable SSH on a headless Raspberry PI](https://www.raspberrypi.org/documentation/remote-access/ssh/)
 by placing a file named `ssh` in the boot partition of the SD card.
* Connect the Raspberry Pi to an ethernet port on your router.
* Log into using the default username `ubuntu` and password `ubuntu`.
* Configure wifi following these
  [https://raspberrypi.stackexchange.com/a/111787/120469](instructions).
* Install the dependencies,
```
wget https://raw.githubusercontent.com/wil3/jackcast/master/platforms/ubuntu/install.sh .
chmod +x install.sh
sudo install.sh
```
* Clone the repo and install Jackcast
```
mkdir -p /srv/www
cd /srv/www
git clone https://github.com/wil3/jackcast.git
cd jackcast
python3 -m venv env
source env/bin/activate
pip3 install .
```
* Configure Nginx
```
sudo rm /etc/nginx/sites-enabled/default
cp /srv/www/jackcast/platforms/ubuntu/etc/nginx/sites-available/jackcast
/etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/jackcast /etc/nginx/sites-enabled
```
* Install the Jackcast service 
```
sudo cp /srv/www/jackcast/platforms/ubuntu/etc/systemd/user/jackcast.service
/etc/systemd/user/
```
* Reboot
```
sudo reboot
```
* Jack cast should now be accessible by a browser at `jackcast.local`. 

Note this has only been tested on Android 10 Firefox 68.8.1, and Ubuntu 18.04
Firefox 69.0.2. I have experienced issues not being able to resolve the local
domain via mDNS on Android 6. In this case you need to access by IP address.

## Stack
* Raspberry Pi 4
* Ubuntu Server 20.04
* Nginx
* Gunicorn
* Flask
* JQuery + Materialize CSS

## Sample Parts List 

| Price | Item |
| ------| -----|
| $35.00 | [Raspberry Pi 4 2GB](https://www.microcenter.com/product/621439/raspberry-pi-4-model-b---2gb-ddr4)|
| $4.49  | [Micro Center 32GB microSDHC Class 10 Flash Memory Card](https://www.microcenter.com/product/485584/micro-center-32gb-microsdhc-class-10-flash-memory-card) | 
| $7.99  | [Raspberry Pi 4 Official 15W Power Supply](https://www.microcenter.com/product/608170/raspberry-pi-4-official-15w-power-supply-us---black) | 
| $7.99  | [USB External Stereo Sound Adapter](https://www.amazon.com/gp/product/B00OJ5AV8I/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1) | 
| Free   | [Raspberry Pi 4 case (Free if you have a 3D printer)](https://www.thingiverse.com/thing:3723561) |

Total Cost: $55.47

![Jackcast](https://github.com/wil3/jackcast/blob/master/.github/images/pi-jackcast.jpg)
