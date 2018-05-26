From ubuntu:16.04

RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak

COPY sources.list /etc/apt/sources.list

COPY screenrc /root/.screenrc

RUN apt-get -y update

RUN apt-get install -y build-essential vim git wget command-not-found m4 unzip time python python-pip screen curl

RUN wget https://raw.github.com/ocaml/opam/master/shell/opam_installer.sh -O - | sh -s /usr/bin

RUN git clone https://github.com/frenetic-lang/frenetic.git

WORKDIR /root/frenetic

ENV PATH /usr/local/bin/:/root/.opam/4.06.0/bin/:$PATH

RUN opam init -y

RUN opam switch -y 4.06.0

RUN opam install -y jbuilder opam-installer

RUN opam install -y cohttp-async async_extended tcpip yojson sedlex mparser cstruct-async open ppx_deriving

# RUN jbuilder external-lib-deps --missing @install

ENTRYPOINT ["/bin/bash"]
