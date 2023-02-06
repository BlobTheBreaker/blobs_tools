#!/usr/bin/python

# Brief:
############################################
# Mini script to filter out some domains
# from input files. Might add options later
# for now idc.


import sys


if len(sys.argv) != 2:
	print("Usage: " + sys.argv[0] + " input file")

f = open(sys.argv[1])
for line in f.readlines():
    sanitized = line.replace("\n", "").replace("\t", "")
    topLevel = sanitized.split('.')[-1]
    domain = sanitized.split('.')[0]
    if domain[0] != "p" or domain[-1] != "x":
        continue
    if topLevel != "com":
        continue
    print(sanitized)

f.close()
