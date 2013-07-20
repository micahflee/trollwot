#!/usr/bin/env python

import sys, time
cwd = sys.path[0]

sys.path.append(cwd+'/lib/python-gnupg')
import gnupg

if __name__ == '__main__':
    # arguments
    if len(sys.argv) != 3:
        print 'Usage: {0} [ascii_art.txt] [keyid]'.format(sys.argv[0])
        sys.exit()
    ascii_filename = sys.argv[1]
    keyid = sys.argv[2]
    keyserver_url = "http://pgp.mit.edu:11371/pks/lookup?op=vindex&search=0x{0}".format(keyid)

    # download the key to sign
    gpg = gnupg.GPG(gnupghome=cwd+'/homedir_ascii_sign', gpgbinary=cwd+'/lib/gnupg/g10/gpg', verbose=False)
    gpg.recv_keys('pgp.mit.edu', keyid)

    # prep new keys
    for userid in open(ascii_filename, 'r').read().strip().split('\n'):
        print "Generating key with userid: {0}".format(userid)
        input = gpg.gen_key_input(name_real = userid, name_comment = 'Trolling the Web of Trust')
        key = gpg.gen_key(input)
        pubkey = gpg.export_keys(key.fingerprint)
        seckey = gpg.export_keys(key.fingerprint, True)
        gpg.import_keys(seckey)

