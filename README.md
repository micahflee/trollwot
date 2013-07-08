Trolling the Web of Trust
=========================

This repository is the home of scripts related to my OHM2013 talk.

To get started, clone the repo and submodules:

    git clone https://github.com/micahflee/trollwot.git
    cd trollwot
    git submodule init
    git submodule update

Install the gnupg build dependencies. On a Debian-based distro you do this:

    sudo apt-get build-dep gnupg

Build the modified gnupg.

    cd lib/gnupg
    ./configure
    make

Download the web of trust
-------------------------

I wrote a script to recursively download the web of trust, one key at a time. However it's horrible ineffecient and will take forever to finish running. To start downloading the web of trust:

    ./download_strong_set.py

A better way to get public keys is to download a recent static dump of all the keys in the public key servers from one of these places:

* ftp://ftp.prato.linux.it/pub/keyring/dump-latest/
* http://keyserver.borgnet.us/dump/
