import soco
from jackcast.logger import jackcast_logger
from jackcast.speakers import AudioNetwork, Speaker

log = jackcast_logger.get_logger(__name__)


class Sonos(AudioNetwork):
    """With sonos we can have multiple speakers playing"""
    def __init__(self, server_port=80):
        """

        Args:
            server_port: (int) This is the port a client connects to web server.
            If this application is behind a proxy the port must be the public
            facing web server port.
        """

        self.uri = 'x-rincon-mp3radio://{}:{}/cast'.format(self.get_ip_addr, server_port)
        # The coordinator is the speaker we communicate with. If there is a
        # group it will forward the request to the other speakers.
        self.coordinator = None

        # Init an active speaker
        devices = soco.discover()
        if devices:
            for device in devices:
                info = device.get_current_transport_info()
                # TODO (wfk) check if there are more than one then find the
                # coordinator
                if info['current_transport_state'] == 'PLAYING':
                    self.coordinator = device

    def set_volume(self, volume):
        if self.coordinator:
            self.coordinator.group.volume = volume

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
        devices = soco.discover()
        if devices:
            for device in soco.discover():
                info = device.get_current_transport_info()
                if info['current_transport_state'] == 'PLAYING':
                    status = Speaker.STATUS_PLAYING
                else:
                    status = Speaker.STATUS_STOPPED
                speaker = Speaker(device.player_name, device.volume, status)
                speakers.append(speaker)

                self._log_device(device)

        return speakers

    def set_active(self, device_names):
        """Set the device names as active

        Args:
            names: A list of device names to set active.
        """
        log.info(f"Activating speakers: {device_names}")
        if len(device_names) == 1:
            device = soco.discovery.by_name(device_names[0])
            # Handle the case in which the last device was the coodinator
            # and had other devices in its group which must be removed.
            for player in device.group:
                if player.player_name != device.player_name:
                    player.unjoin()
            self.coordinator = device
        elif len(device_names) > 1:
            # Take the first device and make it the coordinator
            group = [soco.discovery.by_name(name) for name in device_names]
            self.coordinator = group.pop()
            self.coordinator.unjoin()
            log.debug("New coordinator:")
            self._log_device(self.coordinator)

            # Now join the rest of the selected devices to the coordinator
            log.debug("Adding the following devices to the coordinator:")
            for device in group:
                device.join(self.coordinator)
                self._log_device(device)
        else:
            self.coordinator = None

    def stop(self):
        """Stop playing. This means the last enabled device just became
        inactive"""
        if self.coordinator:
            log.info(f"Stopping {self.coordinator.player_name}")
            self._log_device(self.coordinator)
            self.coordinator.unjoin()
            self.coordinator.stop()

    def play(self):
        if self.coordinator:
            log.info((f"Casting audio to {self.coordinator.player_name} "
                          f"at {self.uri}"))
            self.coordinator.play_uri(self.uri, title="Jackcast")

    def _log_device(self, device):
        """Print status of sonos device

        device: a soco.core.SoCo instance
        """
        if device:
            log.debug((f"Name={device.player_name} IP={device.ip_address} "
                       f"Group={device.group} Coord={device.is_coordinator} "
                       f"Volume={device.volume}"))
