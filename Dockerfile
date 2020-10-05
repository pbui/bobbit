FROM	    alpine:latest
MAINTAINER  Peter Bui <pbui@yld.bx612.space>

RUN	    apk update && \
	    apk add python3 \
		    py3-feedparser \
		    py3-tornado \
		    py3-yaml \
			  py3-pip \
			  gcc \
			  linux-headers \
			  musl-dev \
			  python3-dev \
		    figlet

ADD	  https://github.com/pbui/bobbit/archive/bobbit-0.2.x.tar.gz /tmp
RUN 	tar xvzf /tmp/bobbit-* -C / && mv /bobbit* /bobbit
RUN		pip3 install -r /bobbit/requirements.txt

ENV 	USER=sample-user
ENTRYPOINT  ["/bobbit/bin/bobbit"]
