from flask import jsonify, render_template, request

from jackcast import app, jc


@app.route('/api/volume', methods=['GET', 'POST'])
def volume():
    """Get or set volume"""
    if request.method == 'POST':
        volume = request.form['volume']
        print("Volume =", volume)
        jc.volume = volume
        jc.speaker.set_volume(volume)
        return jsonify({'success': True})
    else:
        return jsonify({'success': True, 'volume': jc.speaker.volume})


@app.route('/api/speakers', methods=['GET', 'POST'])
def speakers():
    """Get or set speakers to cast to.

    Once a speaker is set start playing audio on it"""
    if request.method == 'POST':
        devices = request.form.getlist('devices[]')

        if len(devices) > 0:
            # no grouping just play on that speaker
            jc.speaker.set_active(devices)
            jc.speaker.set_volume(jc.volume)
            jc.speaker.play()
        else:
            jc.speaker.stop()
            jc.speaker.set_active([])

        return jsonify({'success': True, 'device': {'volume':jc.speaker.volume}})
    else:
        speakers = [vars(speaker) for speaker in jc.speaker.speakers()]

        return jsonify({'success': True, 'speakers': speakers,
                        'volume': jc.speaker.volume})


@app.route('/')
def index():
    return render_template('index.html')
