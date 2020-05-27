FROM	    alpine:latest
MAINTAINER  Peter Bui <pbui@yld.bx612.space>

RUN	    apk update && \
	    apk add python3 \
		    py3-feedparser \
		    py3-tornado \
		    py3-yaml \
		    figlet

RUN	    wget -O - https://github.com/pbui/bobbit/archive/master.tar.gz | tar xzvf -

ENTRYPOINT  ["/bobbit-master/bobbit.sh", "--config-dir=/var/lib/bobbit", "--log-path=/var/lib/bobbit/log"]
