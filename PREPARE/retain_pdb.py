#!/usr/bin/python3
#!codeing:utf-8


"""
Clear pdb structures
Retain only part of pdb
Some line header such as "TITLE", "HEASER" and "END" was retained
"ATOM" and "ANISOU" need more necessary
"""

from os import mkdir
from os import listdir
from argparse import ArgumentParser

Arg = ArgumentParser()
Arg.add_argument("--pdb", "-p", help="PDB files folder name")
arg = Arg.parse_args()

#list "RES" filter header "ANISOU"
RES = ["ALA", "ARG", "PHE", "ILE", "ASP", "PRO", "SER", "CYS", "TYR", 
	   "LEU", "ASN", "GLY", "VAL", "TRP", "LYS", "GLN", "HIS", "THR",
	   "MET", "GLU"]
DIR = "PDB_CLEARER"
mkdir(DIR)

for pdb_name in listdir(arg.pdb):
	"""
	pdb_name is PDB file nema
	"""
	pdb_path = arg.pdb + "/" + pdb_name
	with open(pdb_path, mode="r") as pdb_file:
		pdb_lines = pdb_file.readlines()
	out_path = DIR + "/" + pdb_name
	with open(out_path, mode="a") as out_file:
		for line in pdb_lines:
			if (line[:6].rstrip()=="ATOM") and (line[21]=="A") and (0<int(line[22:26])<1000):
				out_file.write(line)
			elif (line[:6]=="ANISOU") and (line[21]=="A") and (0<int(line[22:26])<1000) and (line[17:20] in RES):
				out_file.write(line)
			elif (line[:6].rstrip()=="TER") and (line[21]=="A"):
				out_file.write(line)
			elif line[:6].rstrip()=="TITLE":
				out_file.write(line)
			elif line[:6].rstrip()=="HEADER":
				out_file.write(line)
			elif line[:6].rstrip()=="MASTER":
				out_file.write(line)
			elif line[:6].rstrip()=="END":
				out_file.write(line)
