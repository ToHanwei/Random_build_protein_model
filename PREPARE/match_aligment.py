#!codeing:utf-8

"""
Sequence fom pdb file are not match fasta sequence sometime
This script will match them
"""

import sys

files = sys.argv[1]
fopen = open(files, "r")

file_list = fopen.readlines()
pdb_seq = file_list[0].split(" ")[1].rstrip()
fas_seq = file_list[1].split(" ")[1].rstrip()

print(pdb_seq)
print(fas_seq)
