#!/usr/bin/python
# Find duplicate files in a directory.
# Baris Metin - baris at metin.org

import os
import re
import sys
import stat
import hashlib
import logging
import optparse

MB = 1024 * 1024
logging_format = "%(levelname)s %(asctime)s: %(message)s"

def read_sample_content(path, size):
    sample_content = ""
    if size < MB:
        sample_content = open(path, 'r').read()
    else:
        fd = os.open(path, os.O_RDONLY)
        read_size = MB / 2
        sample_content += os.read(fd, read_size)
        remaning_size = size - read_size
        if remaning_size > read_size:
            seek_length = size - read_size
            os.lseek(fd, seek_length, os.SEEK_SET)
            sample_content += os.read(fd, read_size)
        os.close(fd)
    return sample_content
    

def sample_file(path):
    size = os.stat(path).st_size
    sample_content = read_sample_content(path, size)
    return "%s_%d" % (hashlib.sha1(sample_content).hexdigest(), size)
    

def walk(path, options):
    samples = {} # {sample: [filepath,]}
    for dirpath, dirnames, filenames in os.walk(path):
        match = [e for e in options.excludes if e.match(dirpath)]
        if match:
            logging.debug("Skipping path %s, is excluded" % dirpath)
            dirnames[:] = [] # do not walk through sub-directories
            continue
                
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.islink(filepath) or not os.path.isfile(filepath):
                logging.debug("Skipping %s, not a proper file" % filepath)
                continue
            logging.debug("Working on %s" % filepath)
            sample = sample_file(filepath)
            entry = samples.get(sample, [])
            entry.append(filepath)
            samples[sample] = entry
    return samples


def duplicates(paths, options):
    samples = {}
    for path in paths:
        cur_samples = walk(path, options)
        samples.update(cur_samples)
    return samples


def report(samples):
    logging.info("Sampled %s files" % len(samples))
    for sample in samples:
        if len(samples[sample]) > 1:
            print "Duplicate:", samples[sample]


def main():
    parser = optparse.OptionParser()
    parser.add_option(
        "-e", "--exclude",
        dest = "excludes", action = "append", default = [],
        help = "Exclude a directory from search path using regex expressions."
        )
    parser.add_option(
        "--debug", action="store_true",
        dest = "debug",
        help = "Enable debug messages."
        )
    options, args = parser.parse_args()
    try:
        options.excludes = [re.compile(e) for e in options.excludes]
    except:
        logging.fatal("Invalid exclude expression. Verify all exludes are valid regex expressions.")
        sys.exit(-1)
    if options.debug:
        logging.basicConfig(level = logging.DEBUG, format=logging_format)
    else:
        logging.basicConfig(level = logging.INFO, format=logging_format)
    if args:
        samples = duplicates(args, options)
        report(samples)
    else:
        parser.print_help()
        sys.exit(-1)


if __name__ == "__main__":
    main()
