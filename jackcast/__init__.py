from flask import Flask
from jackcast.speakers.sonos import sonos_app, Sonos

class JackcastCtl:
    """The intent of this class is to be the master controller for Jackcast.
    As we expand to support additional network speakers the """
    def __init__(self):
        # The master volume
        self.volume = 0
        # The currently active speaker implementing a AudioNetwork class
        self.speaker = None

jc = JackcastCtl()
jc.speaker = Sonos(80)
app = Flask(__name__)
app.register_blueprint(sonos_app)

import jackcast.views

