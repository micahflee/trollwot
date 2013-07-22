#!/usr/bin/env python

import sys, os, subprocess, threading
from time import time
cwd = sys.path[0]

class BruteForceKeyID_Common:
    def __init__(self, keyid, userid):
        self.start_time = int(time())
        self.keyid = keyid
        self.userid = userid
        self.rsa_count = 0
        self.tries = 0
        self.gpg_homedir_count = 0
        self.found = False

        self.timestamp_now = int(time())
        self.timestamp_last_year = self.timestamp_now - 60*60*24*365

        self.ssh_homedir = '{0}/bruteforce_keyid_data/{1}/ssh'.format(cwd, self.start_time)
        self.new_dir(self.ssh_homedir)

        self.new_gpg_homedir()
        

    def new_dir(self, path):
        if not os.path.exists(path):
            try:
                os.makedirs(path, 0700)
            except Exception, e:
                print "Error making dir {0}: {1}".format(path, e)
                return False
        return True

    def new_gpg_homedir(self):
        self.gpg_homedir_count += 1
        self.gpg_homedir = '{0}/bruteforce_keyid_data/{1}/gpg/{2}'.format(cwd, self.start_time, self.gpg_homedir_count)
        self.new_dir(self.gpg_homedir)

class BruteForceKeyID(threading.Thread):
    def __init__(self, common):
        self.common = common

        while not self.common.found:
            self.gen_rsa()
            print 'Starting brute force'
            for timestamp in range(self.common.timestamp_last_year, self.common.timestamp_now)[::-1]:
                fingerprint = self.gen_openpgp(timestamp)
                if self.common.found:
                    break

    def gen_rsa(self):
        # generating RSA key
        self.common.rsa_count += 1
        print "Generating a new RSA key {0}/{1}".format(self.common.ssh_homedir, self.common.rsa_count)
        subprocess.Popen('ssh-keygen -f {0}/{1} -P "" -q'.format(self.common.ssh_homedir, self.common.rsa_count), shell=True).wait()

    def gen_openpgp(self, creation_timestamp):
        # convert it to an openpgp key
        os.environ['PEM2OPENPGP_KEY_TIMESTAMP'] = str(creation_timestamp)
        p = subprocess.Popen('{0}/lib/monkeysphere-0.35/src/pem2openpgp "{1}" < {2}/{3} | gpg --homedir {4} --import'.format(cwd, self.common.userid, self.common.ssh_homedir, self.common.rsa_count, self.common.gpg_homedir), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in p.stderr.readlines():
            if 'secret key imported' in line:
                keyid = line.split()[2].split(':')[0]
                if keyid == self.common.keyid:
                    print '\nGenerated collision! Ran in {0} seconds'.format(self.common.start_time)
                    subprocess.Popen(['gpg', '--homedir', self.gpg_homedir, '--fingerprint', '--list-keys', keyid])
                    self.common.found = True
                else:
                    time_diff = int(time() - self.common.start_time)
                    try:
                        keys_per_sec = int(self.common.tries / time_diff)
                    except:
                        keys_per_sec = 0
                    sys.stdout.write('\r[ seconds: {0} ] [ tries: {1} ] [ keys per second: {2} ] [ gpg homedirs: {3}] '.format(time_diff, self.common.tries, keys_per_sec, self.common.gpg_homedir_count))
                    sys.stdout.flush()
        
        self.common.tries += 1
        if self.common.tries % 1000 == 0:
            self.common.new_gpg_homedir()

if __name__ == '__main__':
    # arguments
    if len(sys.argv) < 3:
        print 'Usage: {0} [8-digit keyid] [user id] [threads=4]'.format(sys.argv[0])
        sys.exit()
    keyid = sys.argv[1]
    userid = sys.argv[2]
    
    if len(sys.argv) == 4:
        try:
            thread_count = int(sys.argv[3])
        except:
            thread_count = 4
    else:
        thread_count = 4

    # start
    common = BruteForceKeyID_Common(keyid, userid)

    print "Searching for keyid {0} using {1} threads".format(keyid, thread_count)
    for i in xrange(thread_count):
        BruteForceKeyID(common)

