Trolling the Web of Trust
=========================

This repository is the home of scripts related to my OHM2013 talk.

To get started, clone the repo and submodules:

    git clone https://github.com/micahflee/trollwot.git
    cd trollwot
    git submodule init
    git submodule update

Install some dependencides. On a Debian-based distro you do this:

    sudo apt-get install python-psutil monkeysphere

Install the gnupg build dependencies. On a Debian-based distro you do this:

    sudo apt-get build-dep gnupg

Build the modified gnupg.

    cd lib/gnupg
    ./configure
    make

ASCII sign a PGP key
--------------------

ascii_sign is a script that takes a filename and a target key id as input. It downloads the target key, then generates a new PGP for each line in the file. It signs the target key with the new keys and pushes everything to the pgp.mit.edu key server. Essentially, it lets you sign any key with ASCII art.

For example, check out my key: http://pool.sks-keyservers.net:11371/pks/lookup?op=vindex&search=0x5C17616361BD9F92422AC08BB4D25A1E99999697

ASCII sign a key like this:

    ./ascii_sign [ASCII_ART_FILENAME] [KEYID]

If you're ASCII signing a key with multiple user IDs, you'll have to press "y" to verify you want to sign all user IDs for each line.

Add fake sigs to a PGP key
--------------------------

fake_sign.py is a script that takes a name, email address, and target key id as input. It creates a new key with that name and email, and uses it to sign the target key.

For example, if you want Barack Obama to sign your key, it's easy:

    ./fake_sign [NAME] [EMAIL] [KEYID]

Brute force PGP key ID
----------------------

bruteforce_keyid.py is a modified version of the keytrans script, that comes with [monkeysphere](http://web.monkeysphere.info/) that adds new functionality to do the brute forcing. Since:

    fingerprint = hash(public_key)
    public_key = timestamp + public_key_data

Therefore:

    fingerprint = hash(timestamp + public_key_data)

So the script works like this:

* It generates a 4096 bit RSA key
* It sets the creation timestamp to now
* It goes in a loop calculating the fingerprint and looking for collisions, decrementing the timestamp until the timestamp is from 3 years ago
* If it didn't find it, it starts over by generating a new 4096 bit RSA key

On my laptop it compares about 12,000 fingerprints per second. Here's how to use it:

    ./bruteforce_keyid [USERID] [KEYID]

