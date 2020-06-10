# Start the flask app in development mode
# Useful for running locally and doing development/testing
export FLASK_APP=jackcast
export FLASK_ENV=development
ip4=$(/sbin/ip -o -4 addr list wlan0 | awk '{print $4}' | cut -d/ -f1)
flask run --host=$ip4 --port=5000
