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

Brute force PGP key ID (inefficiently)
--------------------------------------

The script that brute forces key IDs uses a modified version of gnupg that removes all the entropy from key generation, which makes it very quick and very insecure. To run it on your computer, making it a very high priority process:

    nice -20 ./brute_force_keyid.py

Although it actually turns out that this is an inefficient way to brute force key IDs.
