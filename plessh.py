#!/usr/bin/env python
#
# plessh will run the given shell command on all Planetlab Europe
# nodes.
#

import sys
import os
import xmlrpclib
from threading import Thread
from getpass import getpass

KEY_FILE = "~/.ssh/id_rsa"
BASE_CMD = 'ssh -q %(options)s -i %(key)s -l root %(host)s "%(cmd)s"'
THREAD_COUNT = 10
SSH_OPTIONS = {
    "BatchMode": "yes",
    "StrictHostKeyChecking": "no",
    "ConnectTimeout": 30,
    "UserKnownHostsFile": "/dev/null",
    "CheckHostIP": "no"
    }

class API:
    def __init__(self, hostname, username, password):
        self.host = hostname
        self.api = xmlrpclib.ServerProxy("https://%s/PLCAPI/" % self.host, allow_none=True)
        self.auth = {
            "Username": username,
            "AuthString": password,
            "AuthMethod": "password"
            }
        # this will raise an exception if not successful
        self.api.AuthCheck(self.auth)

    def wrap(self, function):
        def wrapper(*args):
            args = (self.auth, ) + args
            return function(*args)
        return wrapper

    def __getattr__(self, attr):
        return self.wrap(getattr(self.api, attr))


def getAPI(hostname, username=None, password=None):
    if not username: username=raw_input("PLE username: ")
    if not password: password=getpass("PLE password: ")
    while True:
        try:
            return API(hostname=hostname, username=username, password=password)
        except xmlrpclib.Fault,e:
            print e
            print "Please try again."
            username=raw_input("PLE username: ")
            password=getpass("PLE password: ")
            continue


class Command(Thread):
    def __init__(self, cmd, hosts=[]):
        Thread.__init__(self)
        self.hosts = hosts
        self.cmd = cmd
        self.results = {}

    def runCmd(self, host):
        cmd = BASE_CMD % {'cmd': self.cmd,
                          'host': host,
                          'key': KEY_FILE,
                          'options':  " ".join(["-o %s=%s" % (o,v) for o,v in SSH_OPTIONS.items()])}
        print "Running on %s ..." % host
        p = os.popen(cmd)
        output = p.read().strip()
        if not output:
            output = "No output or can not reach to host"
        return output

    def run(self):
        for host in self.hosts:
            self.results[host] = self.runCmd(host)


def distributeHosts(num_hosts):
    dist_list = []
    host_per_thread = num_hosts / THREAD_COUNT
    rest = num_hosts % THREAD_COUNT
    for i in range(THREAD_COUNT):
        c = host_per_thread
        if rest:
            c += 1
            rest -= 1
        dist_list.append(c)
    return dist_list


def main(plchost, cmd, print_report=lambda:None):
    ple = getAPI(plchost)
    local_nodes = [n['hostname'] for n in ple.GetNodes({'peer_id':None})]
    dist_list = distributeHosts(len(local_nodes))
    thread_list = []
    index = 0
    for i in range(THREAD_COUNT):
        current = Command(cmd, local_nodes[index:index+dist_list[i]])
        index += dist_list[i]
        thread_list.append(current)
        current.start()
    for i in thread_list:
        i.join()

    results = {}
    for i in thread_list:
        results.update(i.results)

    print_report(results)

if __name__ == "__main__":
    def save_report(results, fname="command_report.txt"):
        reverse_results = {}
        for node in results.keys():
            if reverse_results.has_key(results[node]):
                reverse_results[results[node]].append(node)
            else:
                reverse_results[results[node]] = [node,]

        f = open(fname, "w")
        for result in reverse_results.keys():
            f.write("%s (%d):\n" % (result, len(reverse_results[result])))
            for node in reverse_results[result]:
                f.write("\t%s\n"% node)
            f.write("\n\n")
        f.close()
        print "Please see the command report in %s." % fname

    main("www.planet-lab.eu", sys.argv[1], print_report=save_report)
