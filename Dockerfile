FROM python:3.8-alpine as jackcast-base
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-static /bin/tini
RUN chmod +x /bin/tini
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN apk add --no-cache alsa-lib-dev alsa-utils alsa-utils-doc alsa-lib alsaconf pulseaudio pulseaudio-utils avahi libffi-dev
RUN pip install --no-cache-dir -r requirements.txt 
RUN echo "load-module module-null-sink sink_name=Jackcast sink_properties=\"device.description='Jackcast'\"" >>  /etc/pulse/default.pa
RUN echo "load-module module-loopback latency_msec=5 sink=Jackcast" >> /etc/pulse/default.pa  

WORKDIR /app
COPY . ./
ENTRYPOINT ["tini", "--"]

FROM jackcast-base as jackacast-deploy
EXPOSE 5000
ENV PYTHONPATH=/app
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]