import socket
import subprocess

from flask import Blueprint, Response


class AudioNetwork:
    @property
    def get_ip_addr(self):
        # TODO (wfk) do the devices use mDNS? If so we can just use our hostname.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_addr = s.getsockname()[0]
        s.close()
        return ip_addr

    """Create a generic audio network"""
    def set_volume(self, volume):
        raise NotImplemented("Not implemented")

    def volume(self):
        raise NotImplemented("Not implemented")

    def speakers(self):
        """Return a list of available devices"""
        raise NotImplemented("Not implemented")

    def stop(self):
        raise NotImplemented("Not implemented")

    def play(self):
        raise NotImplemented("Not implemented")


class Speaker:
    STATUS_PLAYING = 'PLAYING'
    STATUS_STOPPED = 'STOPPED'

    def __init__(self, name, volume, status):
        self.name = name
        self.volume = volume
        self.status = status


speaker_app = Blueprint('speaker_app', __name__)


@speaker_app.route('/cast')
def cast():
    return Response(gen_audio(), mimetype='audio/mpeg')


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
