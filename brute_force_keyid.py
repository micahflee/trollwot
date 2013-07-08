#!/usr/bin/env python

import sys
from time import time
cwd = sys.path[0]

sys.path.append(cwd+'/lib/python-gnupg')
import gnupg

class TrollWoT_GenKeyID:
    def __init__(self, gpg):
        self.gpg = gpg

    def bruteforce(self, keyid, name_real, name_email, name_comment='', key_type='RSA', key_length=1024):
        sys.stdout.write('Brute forcing key id {0}\n'.format(keyid))
        start_time = time()

        input = self.gpg.gen_key_input(name_real=name_real, name_email=name_email, name_comment=name_comment, key_type=key_type, key_length=key_length)
        tries = 0
        while True:
            key = self.gpg.gen_key(input)
            if key.fingerprint[-len(keyid):] == keyid:
                sys.stdout.write('\nFound collision! Fingerprint: {0}'.format(key.fingerprint))
                break
            
            tries += 1
            time_diff = int(time() - start_time)
            try:
                keys_per_sec = int(tries / time_diff)
            except:
                keys_per_sec = 0

            sys.stdout.write('\r[ {0} seconds ]   [ {1} tries ]   [ keys per second: {2} ]          '.format(time_diff, tries, keys_per_sec))
            sys.stdout.flush()

        time_diff = int(time() - start_time)
        sys.stdout.write('\nRan in {0} seconds\n'.format(time_diff))

if __name__ == '__main__':
    gpg = gnupg.GPG(gnupghome=cwd+'/homedir_brute_force_keyid', gpgbinary=cwd+'/lib/gnupg/g10/gpg', verbose=False)

    gen_keyid = TrollWoT_GenKeyID(gpg)
    gen_keyid.bruteforce(keyid='99999697', name_real='Test Key', name_email='testkey@micahflee.com')

