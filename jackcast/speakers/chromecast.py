from jackcast.logger import jackcast_logger
from jackcast.speakers import AudioNetwork

log = jackcast_logger.get_logger(__name__)


class Chromecast(AudioNetwork):
    def __init__(self):
        pass

    def set_volume(self, volume):
        pass

    def speakers(self):
        pass

    def stop(self):
        pass

    def play(self):
        pass
