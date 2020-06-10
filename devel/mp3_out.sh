# Helper script to test that we are getting audio data flowing through the
# entire pipeline and output as an mp3
parec --format=s16le -d Jackcast.monitor | lame -b 192 -r -
