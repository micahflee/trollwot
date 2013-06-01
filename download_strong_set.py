#!/usr/bin/env python

import sys
cwd = sys.path[0]

sys.path.append(cwd+'/lib/python-gnupg')
import gnupg

if __name__ == '__main__':
    print 'Download the strong set, starting with 99999697'
    gpg = gnupg.GPG(gnupghome=cwd+'/homedir')

    # import micahflee.asc
    gpg.import_keys(open(cwd+'/micahflee.asc', 'r').read())


