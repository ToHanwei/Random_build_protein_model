#!/bin/python

"""
Rename number of pdb file resduce number
You should give a start resduce number
The script will numbering in sequence, and ruturn end number
"""

from sys import argv

start = int(input("Input start number: ")) - 1
pdb_file = open(argv[1], "r")
pdb = pdb_file.readlines()

#outfile name
outname = argv[1].split(".")[0] + "_rename.pdb"

pdb_out = open(outname, "w")

temp = 0
for line in pdb:
	if line[:6].rstrip() in ["ATOM", "ANISOU"]:
		resid = line[22:26]
		if temp != int(resid):
			start += 1
			temp = int(resid)
		inres = (4-len(str(start)))*" "+str(start)
		line = line[:22] + inres + line[26:]
	pdb_out.write(line)

outstr ="The end resude number is: {0}".format(start)
print("\033[1;31;40m")
print("*"*(len(outstr)+10))
print("*"+" "*4+outstr+" "*4+"*")
print("*"*(len(outstr)+10))
print("\033[0m")
