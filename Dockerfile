FROM amd64/ubuntu:18.04

RUN apt-get update
RUN apt-get install -y lsb-release ubuntu-dbgsym-keyring gnupg2
RUN echo "deb http://ddebs.ubuntu.com $(lsb_release -cs) main restricted universe multiverse\ndeb http://ddebs.ubuntu.com $(lsb_release -cs)-updates main restricted universe multiverse\ndeb http://ddebs.ubuntu.com $(lsb_release -cs)-proposed main restricted universe multiverse" | tee -a /etc/apt/sources.list.d/ddebs.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F2EDC64DC5AEE1F6B9C621F0C8CAB6595FDFF622
RUN cat /etc/apt/sources.list.d/ddebs.list
RUN apt-get update

WORKDIR /
