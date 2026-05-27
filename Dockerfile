FROM	    debian:trixie-slim
MAINTAINER  Peter Bui <pbui@bx612.space>

ENV	    DEBIAN_FRONTEND="noninteractive"

RUN	    apt install --update -y \
		python3 \
		python3-aiohttp \
		python3-dateutil \
		python3-feedparser \
		python3-gdbm \
		python3-icalendar \
		python3-yaml && \
	    apt clean && \
	    rm -rf /var/lib/apt/lists/*

#ADD	    https://github.com/pbui/bobbit/archive/bobbit-0.2.x.tar.gz /tmp
#RUN	    tar xvzf /tmp/bobbit-* -C / && mv /bobbit* /bobbit
COPY	    . /bobbit

ENTRYPOINT  ["/bobbit/bin/bobbit"]
CMD	    ["--config-dir=/srv/bobbit"]
