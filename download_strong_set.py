#!/usr/bin/env python

"""
I started writing this, and then quickly realized it would take a really long 
to actually download the whole strong set this way. Then I began searching for
how to sync from key servers, which lead me to regular static key server dumps:

ftp://ftp.prato.linux.it/pub/keyring/ - Generated every Wednesday
http://keys.niif.hu/keydump/ - Generated every Monday
http://key-server.de/dump - Generated every Friday
ftp://key-server.de/dump (anonymous) - Generated every Friday
http://keyserver.borgnet.us/dump - Generated every Sunday

Right now this script is in a semi-broken state, but I decided to leave it 
here anyway.
"""

import sys, time
cwd = sys.path[0]

sys.path.append(cwd+'/lib/python-gnupg')
import gnupg

class TrollWoT_DownloadWoT:
    def __init__(self, gpg, keyserver = 'pool.sks-keyservers.net'):
        self.gpg = gpg
        self.keyserver = keyserver

        self.imported_long_key_ids = []

        keys = gpg.list_keys()
        fingerprints = []
        for key in keys:
            fingerprints.append(key['fingerprint'])
        self.add_key_ids(fingerprints)
        print 'already have {0} keys in keyring'.format(len(self.imported_long_key_ids))
        
    def download(self, fingerprints):
        sig_fingerprints = []

        i = 0
        for fp in fingerprints:
            if fp not in self.imported_long_key_ids:
                print '{0}: downloading key {1}'.format(i, fp)
                res = self.gpg.recv_keys(self.keyserver, fp)
                self.add_key_ids(res.fingerprints)
            else:
                print '{0}: already have {1}'.format(i, fp)

            sigs = gpg.list_sigs(fp[-8:])
            sig_fingerprints += sigs

            i += 1

        sig_fingerprints_to_import = []
        for fp in sig_fingerprints:
            if fp not in self.imported_long_key_ids:
                sig_fingerprints_to_import.append(fp)

        if len(sig_fingerprints_to_import) > 0:
            print 'downloading {0} more fingerprints'.format(len(sig_fingerprints_to_import))
            self.download(sig_fingerprints_to_import)

    def add_key_ids(self, fingerprints):
        for fp in fingerprints:
            long_key_id = fp[-16:]
            if long_key_id not in self.imported_long_key_ids:
                self.imported_long_key_ids.append(long_key_id)

        
if __name__ == '__main__':
    start_time = time.time()

    print 'Download the strong set, starting with 5C17616361BD9F92422AC08BB4D25A1E99999697'
    gpg = gnupg.GPG(homedir=cwd+'/homedir_download_strong_set', verbose=False)

    download_wot = TrollWoT_DownloadWoT(gpg)
    download_wot.download(['5C17616361BD9F92422AC08BB4D25A1E99999697'])

    end_time = time.time()
    time_diff = int(end_time - start_time)
    print '{0} keys imported, took {1} seconds'.format(len(download_wot.imported_long_key_ids), time_diff)

