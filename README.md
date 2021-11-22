# Jackcast
Jackcast is a device used to stream/cast line-in (auxiliary input) audio to a wireless device. Use this device to cast audio from a record player or other old sound systems. 

This software is intended to run on a computer like a Raspberry Pi that can be permanently connected to the audio device. Jackcast includes a webapp to control the wireless device such as the volume and which device to stream too. Jackcast has no concept or control of where the line-in audio is coming from which is why there are no controls to play, pause and change the track.

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

* Use the [Raspberry Pi Imager](https://www.raspberrypi.org/documentation/installation/installing-images/) to install Ubuntu Server 20.04 (tested with 32bit version)

  ![Ubuntu version](https://github.com/wil3/jackcast/blob/master/.github/images/ubuntu-version.png)

* [Enable SSH on a headless Raspberry PI](https://www.raspberrypi.org/documentation/remote-access/ssh/) by placing a file named `ssh` in the boot partition of the SD card.

* Connect the Raspberry Pi to an ethernet port on your router.

* Log into using the default username `ubuntu` and password `ubuntu`.

* Configure wifi following these [Enable WIFI on Ubuntu 20.04](https://raspberrypi.stackexchange.com/a/111787/120469).

* Install the dependencies and jackcast - this will ask you for a hostname to set on the rpi - the default is jackcask

* **IMPORTANT NOTE** - please plug in the usb sound card (specifically the Behringer UCA202 - as pulse audio doesn't seem to be able to pick it up if its not plugged in after the install)
```
wget https://raw.githubusercontent.com/wil3/jackcast/master/platforms/ubuntu/install.sh .
chmod +x install.sh
sudo install.sh
```
* Reboot
```
sudo reboot
```
* Jack cast should now be accessible by a browser at `jackcast.local`. (If you used the default hostname - please replace `jackcast` with what ever hostname you set during install)

**Note**: *this has only been tested on Android 10 Firefox 68.8.1, and Ubuntu 18.04 Firefox 69.0.2. I have experienced issues not being able to resolve the local domain via mDNS on Android 6. In this case you need to access by IP address.*

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

## Alternative Sound Card

| Price   | Item                                                         |
| ------- | ------------------------------------------------------------ |
| $ 28.43 | [Behringer UCA202 U-Control Ultra low-latency 2 In/2 Out USB/Audio Interface](https://www.amazon.com/BEHRINGER-Box-RCA-Phono-UCA202/dp/B000KW2YEI/ref=sr_1_2?keywords=Behringer+UCA202+U-Control+Ultra+low-latency+2+In%2F2+Out+USB%2FAudio+Interface&qid=1637553736&sr=8-2) |

As per https://github.com/wil3/jackcast/issues/10 @**[dangermouse69](https://github.com/dangermouse69)** found that this USB sound card has beter sound quality and it is plug and play.
