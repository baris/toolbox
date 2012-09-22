#!/usr/bin/python

import os
import re
import sys
import json
    
py_file = sys.modules[__name__].__file__
json_file = os.path.splitext(py_file)[0] + ".json"
processes = json.loads(open(json_file).read())

def format(process):
    return "%s\n%s\n" % (
        process,
        processes[process]
    )

found = []
for process in processes:
    for search_re in sys.argv[1:]:
        if re.search(search_re, process, re.IGNORECASE):
            found.append(process)


if found:
    print
    print "\n".join([format(process) for process in found])
    print
    print "Data fetched from triviaware.com/macprocess/all"
    print "Visit http://triviaware.com/macprocess/ for more."
