From ubuntu:16.04

WORKDIR /root

RUN apt-get -y update

RUN apt-get install -y build-essential vim git wget command-not-found m4 unzip time python python-pip screen curl python-pycurl tzdata sudo python-software-properties python-networkx python-dev hping3

COPY screenrc /root/.screenrc

RUN git clone https://github.com/frenetic-lang/pyretic.git

WORKDIR /root/pyretic

RUN git clone https://github.com/noxrepo/pox.git \
	&& cd pox \
	&& git checkout bab636b



ENTRYPOINT ["/bin/bash"]
