#!/usr/bin/env python

import os
import sys

SVN_ROOT = 'http://svn.planet-lab.org/svn'
SVN_MODULES = {
    'BootCD': ['trunk',],
    'BootManager': ['trunk',],
    'BootstrapFS': ['trunk',],
    'Monitor': ['trunk',],
    'MyPLC': ['trunk',],
    'NodeManager': ['trunk',],
    'NodeUpdate': ['trunk',],
    'PLCAPI': ['trunk',],
    'PLCRT': ['trunk',],
    'PLCWWW': ['trunk',],
    'PLEWWW': ['trunk',],
    'PingOfDeath': ['trunk',],
    'build': ['trunk',],
    'drupal': ['trunk',],
    'dummynet_image': ['trunk',],
    'fprobe-ulog': ['trunk',],
    'infrastructure': ['',],
    'ipfw': ['trunk',],
    'iproute2': ['trunk',],
    'iptables': ['trunk','branches/1.3.8'],
    'linux-2.6': ['trunk','branches/22'],
    'madwifi': ['trunk',],
    'nodeconfig': ['trunk',],
    'packet-tracking': ['trunk',],
    'pcucontrol': ['trunk',],
    'pl_sshd': ['trunk',],
    'plcmdline': ['trunk',],
    'pyopenssl': ['trunk',],
    'pypcilib': ['trunk',],
    'pyplnet': ['trunk',],
    'sfa': ['trunk',],
    'tests': ['trunk',],
    'util-vserver': ['trunk',],
    'util-vserver-pl': ['trunk',],
    'vsys': ['trunk',],
    'vsys-scripts': ['trunk',],
    'vsys-wrappers': ['trunk',],
    'www-register-wizard': ['trunk',],
    'yum': ['branches/f12',],
}

GIT_DIR='/home/baris/git'
GITWEB_DIR=os.path.join(os.path.dirname(GIT_DIR), 'gitweb')

def run(cmd):
    print "in", os.getcwd()
    print cmd
    os.system(cmd)

def mdir(module_name, sub='trunk'):
    return os.path.join(GIT_DIR, "%s-%s" % (module_name.lower(), sub.replace('/', '-')))

def main(modules, args):
    if not os.path.exists(GIT_DIR): os.makedirs(GIT_DIR)

    for module in modules:
        for sub in modules[module]:
            d = mdir(module, sub)
            if os.path.exists(d) and os.path.isdir(d):
                os.chdir(d)
                run('git svn rebase')
                os.chdir(GIT_DIR)
            else:
                os.chdir(GIT_DIR)
                run('git svn clone %s/%s/%s %s' % (SVN_ROOT, module, sub, os.path.basename(d)))
            os.chdir(d)
	    run('git update-server-info')

	    gitwebd = os.path.join(GITWEB_DIR, os.path.basename(d) + ".git")
            run('rm -rf %s' % gitwebd)
            run('ln -s %s/.git/ %s' % (d, gitwebd))

            description = "%s %s" % (os.path.join(module, sub), SVN_ROOT+'/'+module+'/'+sub)
            run('echo "%s" > %s/.git/description' % (description, d))

if __name__ == "__main__":
    main(SVN_MODULES, sys.argv)
