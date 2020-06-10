import soco
from jackcast.speakers import AudioNetwork, Speaker

import socket

#from jackcast import app, ctx
import subprocess
from flask import Response,Blueprint
import functools
import os

sonos_app = Blueprint('sonos_app', __name__)

def gen_audio():
    # The following will proxy the null sink to the network
    # This strategy was obtained from the following resources,
    # * https://askubuntu.com/questions/60837/record-a-programs-output-with-
    # pulseaudio
    # * mkchromecast

    # Pulseaudio names the monitor after the module name appended with
    # '.monitor'.
    monitor_name = "{}.monitor".format('Jackcast')
    # Record raw audio coming from the monitoring sink and output to stdout
    parec = subprocess.Popen(['parec', '--format=s16le', '-d', monitor_name],
                             stdout=subprocess.PIPE)
    # Encode the raw audio recording to mp3 and output to stdout
    lame = subprocess.Popen(['lame', '-b', '192', '-r', '-'], 
                            stdin=parec.stdout, stdout=subprocess.PIPE)
    buf_size = 8192
    while True:
        yield lame.stdout.read(buf_size)

@sonos_app.route('/cast')
def cast():
    return Response(gen_audio(), mimetype='audio/mpeg')

class Sonos(AudioNetwork):
    """With sonos we can have multiple speakers playing"""
    def __init__(self, server_port=80):
        """

        Args:
            server_port: (int) This is the port a client connects to web server.
            If this application is behind a proxy the port must be the public
            facing web server port.
        """

        self.uri ='x-rincon-mp3radio://{}:{}/cast'.format(self.get_ip_addr(), server_port) 
        # The coordinator is the speaker we communicate with. If there is a
        # group it will forward the request to the other speakers. 
        self.coordinator = None

        # Init an active speaker
        devices = soco.discover()
        for device in devices:
            info = device.get_current_transport_info()
            # TODO (wfk) check if there are more than one then find the
            # coordinator
            if info['current_transport_state'] == 'PLAYING':
                self.coordinator = device

    def get_ip_addr(self):
        # TODO (wfk) do the devices use mDNS? If so we can just use our hostname.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_addr = s.getsockname()[0]
        s.close()
        return ip_addr

    def set_volume(self, volume):
        if self.coordinator:
            self.coordinator.volume = volume

    @property
    def volume(self):
        if self.coordinator:
            return self.coordinator.volume
        else:
            return 0

    def speakers(self):
        """Return list of all available devices associated with this audio
        connection""" 

        speakers = []
        for device in soco.discover():
            info = device.get_current_transport_info()
            if info['current_transport_state'] == 'PLAYING':
                status = Speaker.STATUS_PLAYING
            else:
                status = Speaker.STATUS_STOPPED
            speaker = Speaker(device.player_name, device.volume, status)
            speakers.append(speaker)

            print ("Name=", device.player_name, 
                   " IP=", device.ip_address, 
                   " Group=", device.group, 
                   " coord=", device.is_coordinator, 
                   " Volume=", device.volume,
                   " Status=", status)

        return speakers

    def set_active(self, name):
        print ("Setting active speaker to ", name)
        self.coordinator = soco.discovery.by_name(name)

    def stop(self):
        if self.coordinator:
            self.coordinator.stop()

    def play(self):
        if self.coordinator:
            print ("Playing to ", self.coordinator.player_name + " uri=", self.uri)
            self.coordinator.play_uri(self.uri, title="Jackcast")

