From ubuntu:16.04

# RUN apt-get -y update

# RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak

# COPY sources.list /etc/apt/sources.list

# RUN cat /etc/apt/sources.list

WORKDIR /root

RUN apt-get -y update

RUN apt-get install -y build-essential vim git wget command-not-found m4 unzip time python python-pip screen curl python-pycurl tzdata

COPY screenrc /root/.screenrc

RUN wget https://raw.github.com/ocaml/opam/master/shell/opam_installer.sh -O - | sh -s /usr/bin

RUN git clone https://github.com/frenetic-lang/frenetic.git

WORKDIR /root/frenetic

ENV PATH /root/.opam/4.06.0/bin/:$PATH

# RUN opam init -y

# RUN opam switch -y 4.06.0

RUN opam init -y --comp=4.06.0

RUN opam update -y

RUN opam install -y jbuilder opam-installer

# RUN opam install -y cohttp-async async_extended tcpip yojson sedlex mparser cstruct-async open ppx_deriving menhir

# RUN jbuilder external-lib-deps --missing @install

RUN pip install ryu

ENTRYPOINT ["/bin/bash"]
