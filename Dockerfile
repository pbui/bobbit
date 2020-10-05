FROM python:3
MAINTAINER  Peter Bui <pbui@yld.bx612.space>

RUN   apt update; apt -y install figlet
ADD   https://github.com/pbui/bobbit/archive/bobbit-0.2.x.tar.gz /tmp
RUN   tar xvzf /tmp/bobbit-* -C / && mv /bobbit* /bobbit
RUN   pip3 install -r /bobbit/requirements.txt

ENV   USER=sample-user
ENTRYPOINT  ["/bobbit/bin/bobbit"]
