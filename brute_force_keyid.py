#!/usr/bin/env python

import sys, threading
from time import time
cwd = sys.path[0]

sys.path.append(cwd+'/lib/python-gnupg')
import gnupg

class BruteForceKeyID_Common:
    def __init__(self, gpg, keyid, name_real, name_email, name_comment='', key_type='RSA', key_length=1024):
        self.collision_key = False
        self.tries = 0

        self.gpg = gpg
        self.keyid = keyid
        self.input = self.gpg.gen_key_input(name_real=name_real, name_email=name_email, name_comment=name_comment, key_type=key_type, key_length=key_length)

class BruteForceKeyID(threading.Thread):
    def __init__(self, common):
        threading.Thread.__init__(self)

        self.common = common

        self.start_time = time()
        self.tries = 0
        
    def run(self):
        while True:
            if self.common.collision_key:
                break

            key = self.common.gpg.gen_key(self.common.input)
            if key and key.fingerprint:
                new_keyid = key.fingerprint[-len(self.common.keyid):]
            else:
                new_keyid = False
            if new_keyid == self.common.keyid:
                sys.stdout.write('\nFound collision! Fingerprint: {0}'.format(key.fingerprint))
                self.common.collision_key = key
                break
            
            self.common.tries += 1
            time_diff = int(time() - self.start_time)
            try:
                keys_per_sec = int(self.common.tries / time_diff)
            except:
                keys_per_sec = 0

            sys.stdout.write('\r[ {0} seconds ]   [ {1} tries ]   [ keys per second: {2} ]          '.format(time_diff, self.common.tries, keys_per_sec))
            sys.stdout.flush()

        time_diff = int(time() - self.start_time)
        sys.stdout.write('\nRan in {0} seconds\n'.format(time_diff))

if __name__ == '__main__':
    # todo: make the keyid and number of threads cli args
    keyid = '99999999'

    gpg = gnupg.GPG(gnupghome=cwd+'/homedir_brute_force_keyid', gpgbinary=cwd+'/lib/gnupg/g10/gpg', verbose=False)
    common = BruteForceKeyID_Common(gpg, keyid=keyid, name_real='Test Key', name_email='testkey@micahflee.com')

    sys.stdout.write('Brute forcing key id {0}\n'.format(keyid))

    # start 4 threads
    for i in xrange(4):
        BruteForceKeyID(common).start()

