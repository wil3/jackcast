class AudioNetwork:
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
