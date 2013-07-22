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

ASCII sign a PGP key
--------------------

ascii_sign.py is a script that takes a filename and a target key id as input. It downloads the target key, then generates a new PGP for each line in the file. It signs the target key with the new keys and pushes everything to the pgp.mit.edu key server. Essentially, it lets you sign any key with ASCII art.

For example, check out my key: http://pool.sks-keyservers.net:11371/pks/lookup?op=vindex&search=0x5C17616361BD9F92422AC08BB4D25A1E99999697

ASCII sign a key like this:

    ./ascii_sign.py [ASCII_ART_FILENAME] [KEYID]

If you're ASCII signing a key with multiple user IDs, you'll have to press "y" to verify you want to sign all user IDs for each line.

Brute force PGP key ID (inefficiently)
--------------------------------------

The script that brute forces key IDs uses a modified version of gnupg that removes all the entropy from key generation, which makes it very quick and very insecure. To run it on your computer, making it a very high priority process:

    nice -20 ./brute_force_keyid.py

Although it actually turns out that this is an inefficient way to brute force key IDs.
