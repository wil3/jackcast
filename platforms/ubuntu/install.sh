# Wget this script to install dependencies

# Install alsa
apt-get install -y\
    libasound2\
    libasound2-plugins\
    alsa-utils\
    alsa-oss

# Install pulse audio 
apt-get install -y\
    pulseaudio\
    pulseaudio-utils

# Set the group for the current user
usermod -aG pulse,pulse-access $USER

# Configure PulseAudio for Jackcast
echo "load-module module-null-sink sink_name=Jackcast sink_properties=\"device.description='Jackcast'\"" >>  /etc/pulse/default.pa
echo "load-module module-loopback latency_msec=5 sink=Jackcast" >> /etc/pulse/default.pa

# Install lame
apt-get install -y\
    lame

hostnamectl set-hostname jackcast

# Enable broadcasting hostname so the server can be accessed by 
# jackcast.local
apt-get install -y avahi-daemon


apt install -y nginx

apt install -y\
    build-essential\
    python3-dev

# required for gunicorn
apt install -y\
    libffi-dev

# Allow HTTP traffic
ufw allow 'Nginx HTTP'

# Since PulseAudio and Jackcast are running as a user service
# we need to make sure the services start on boot. We can do this
# by enable linger per this document,
# https://wiki.archlinux.org/index.php/Systemd/User#Automatic_start-up_of_systemd_user_instances
loginctl enable-linger $USER

