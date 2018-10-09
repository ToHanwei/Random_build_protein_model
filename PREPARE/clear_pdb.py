#!/usr/bin/python3
#!codeing:utf-8

from os import mkdir
from os import listdir
from os import remove
from shutil import move
from os.path import exists
from argparse import ArgumentParser


class Clearer():
	"""
	Need head of line that you want clean up
	Clean up the unwanted parts of pdb format file
	"""
	def __init__(self, pdb, line_header):
		self.pdb = pdb
		self.line_header = line_header
		self.pdblines = []
		#self.pdb_clear = []
	
	def clearup(self):
		"""
		Append line to new list "pdb_clear"
		"""
		pdb_file = open(self.pdb, "r")
		self.pdblines = pdb_file.readlines()
		for line in self.pdblines:
			header = line[:6].rstrip()
			if header in self.line_header:
				pdb_clear.append(line)
		pdb_file.close()

	def write_to_file(self, filee):
		"""
		Write list to file as a new pdb file
		"""
		pdb_clear = list(set(pdb_clear))
		if exists(filee):
			remove(filee)
		outfile = open(filee, "a")
		for line in self.pdblines:
			if line in pdb_clear: continue
			outfile.write(line)
		outfile.close()


class Clear_chain(Clearer):
	def retain_chain(self):
		"""
		Append line to new list, save chain A
		"""
		pdb_file = open(self.pdb, "r")
		self.pdblines = pdb_file.readlines()
		for line in self.pdblines:
			header = line[:6].rstrip()
			if (header in self.line_header)and(line[21] != "A"):
				pdb_clear.append(line)
		pdb_file.close()


def main():
	global pdb_clear
	pdb_clear = []
	NEWF = "CLEAR_PDB"
	HEAD = ["HETATM", "CONECT", "ANISOU", "REMARK"]
	CHAI = ["ATOM", "ANISOU", "TER"]

	#Analytic parameter
	Arg = ArgumentParser()
	Arg.add_argument("--pdb", "-p", help="pdb folder name")
	arg = Arg.parse_args()

	if not exists(NEWF): mkdir(NEWF)
	pdb_names = listdir(arg.pdb)
	for pdb in pdb_names:
		pdb_path = arg.pdb+"/"+pdb
		CHAINclear = Clear_chain(pdb_path, CHAI)
		CHAINclear.retain_chain()
		PDBclear = Clearer(pdb_path, HEAD)
		PDBclear.clearup()
		PDBclear.write_to_file(NEWF+"/"+pdb)
		print(pdb+" is gone!!!")

if __name__ == "__main__":
	main()

