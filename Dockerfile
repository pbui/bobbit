FROM	    alpine:latest
MAINTAINER  Peter Bui <pbui@yld.bx612.space>

RUN	    apk update && \
	    apk add python3 \
		    py3-feedparser \
		    py3-lxml \
		    py3-tornado \
		    py3-twitter \
		    py3-yaml \
		    figlet

RUN	    wget -O - https://gitlab.com/pbui/bobbit-ng/-/archive/master/bobbit-ng-master.tar.gz | tar xzvf -

# Download Hot Fix for feedparser to work on Python 3.7
RUN	    wget -O /usr/lib/python3.7/site-packages/feedparser.py https://gitlab.com/klevstul/muninn/raw/master/additional_resources/feedparser_hotfix/feedparser.py

ENTRYPOINT  ["/bobbit-ng-master/bobbit.py", "--config-dir=/var/lib/bobbit", "--log-file-prefix=/var/lib/bobbit/log"]
