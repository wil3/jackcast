$(function() {

    var slider = document.getElementById("volume-slider");
    noUiSlider.create(slider, {
        start: [0],
        connect: 'lower',
        tooltips: false,
        step: 1,
        orientation: 'horizontal',
        range: {
            'min': 0,
            'max': 100
        },
        format: {
            to: function(value) {
                return value;
            },
            from: function(value) {
                return Number(value);
            }
        }
    });

    function updateVolume(volume) {
        // Update the slider with the provider volume value
        // and update the icon on the volume button
        if (volume == 0) {
            $("#volume-icon").html("volume_mute")
        } else {
            $("#volume-icon").html("volume_up")
        }
        slider.noUiSlider.set(volume);
    }

    function updateVolumeState(enabled) {
        // Update whether the volume is enabled or disabled
        if (enabled) {
            $("#volume-btn").removeClass("disabled");
            slider.removeAttribute("disabled");
        } else {
            $("#volume-btn").addClass("disabled");
            slider.setAttribute("disabled", true);
        }
    }

    function setVolume(volume) {
        $.post("/api/volume", {
            volume: volume
        }, function(res) {
            updateVolume(volume);
        });
    }

    // Get the initial volume value
    $.get('/api/volume', function(data) {
        updateVolume(data.volume);
    });

    // Get the available devices
    $.get('/api/speakers', function(data) {
        if (data.speakers.length > 0) {
            var num_enabled_devices = 0
            ul = $("<ul>");
            data.speakers.forEach(function(speaker) {
                enabled = speaker.status == 'PLAYING'
                num_enabled_devices += enabled
                check = enabled ? 'checked="checked"' : '';
                ul.append(
                    '<li><div class="switch"><label>' +
                    '<input type="checkbox" class="device" ' +
                    check + ' value="' + speaker
                    .name + '" />' +
                    '<span class="lever"></span>' +
                    speaker.name +
                    '</label></div></li>');
            });
            $("#devices").append(ul);
            updateVolumeState(num_enabled_devices > 0);
        } else {
            $("#devices").html("<h5>No devices found</h5>")
        }
    });

    // We must place the listener on the body because this list is
    // dynamically made.
    $("body").on('change', '.device', function() {
        // Callback for when a speaker/device changes state
        var checkedVals = $('.device:checkbox:checked').map(function() {
            return this.value;
        }).get();
        $.post("/api/speakers", {
                "devices": checkedVals
            },
            function(res) {
                updateVolumeState(checkedVals.length > 0);
            }, "json");

    });

    // If the volumen button is clicked, then mute
    $("#volume-btn").click(function() {
        setVolume(0);
    });

    // Update the volume whenever it is checked on the slider
    slider.noUiSlider.on('change', function(volume) {
        volume = volume[0];
        setVolume(volume);
    });

});
