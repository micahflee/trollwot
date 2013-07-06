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

To start downloading the web of trust:

    ./download_strong_set.py
