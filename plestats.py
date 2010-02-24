#!/usr/bin/env python

import xmlrpclib
from getpass import getpass

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


api = API("www.planet-lab.eu", raw_input("user: "), getpass("pass: "))

ple_sites = api.GetSites({"peer_id":None})

def get_users_with_keys(user_ids):
    x = []
    for user_id in user_ids:
        user = api.GetPersons(user_id)[0]
        if user['key_ids']:
            x.append(user_id)
    return x

def get_nodes(site_id):
    return api.GetNodes()

def get_nodes_slivers(site_id):
    slivers=0
    nodes = api.GetNodes({"site_id":site_id})
    for node in nodes:
        slivers += len(node['slice_ids'])
    return (len(nodes), slivers)

print "%s\t%s\t%s\t%s\t%s\n" % ("USER", "SLICE", "NODE", "SLIVER", "SITE NAME")
for site in ple_sites:
    site_user_ids = site['person_ids']
    site_user_ids_with_keys = get_users_with_keys(site_user_ids)
    site_slice_ids = site['slice_ids']

    len_site_nodes, len_site_slivers = get_nodes_slivers(site['site_id'])

    print "%d\t%d\t%d\t%d\t%s" % (len(site_user_ids_with_keys),
                                  len(site_slice_ids),
                                  len_site_nodes,
                                  len_site_slivers,
                                  site['name'])
