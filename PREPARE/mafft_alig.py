#!codeing:utf-8

import os
from sys import argv
from shutil import move
from shutil import rmtree

#"fold" is sequence folder, it's has many sequneces from pdb
#fold = argv[1]
fold = "./PDB_MM_sequence"
#"classA" is classA sequence
#classA = argv[2]
classA = "./classA_data.txt"

class Traverse():
	"""
	Traverse ClassA sequence
	Match the input sequence
	"""
	def __init__(self, seq, fasfold):
		"""
		"seq" is input sequence, that is pdb extract sequence
		"fasfold" is folder that save fasts format file
		"""
		self.seq = seq
		self.fasfold = fasfold
	def write_to_file(self):
		"""
		From "seq" and a corresponding sequence in classA to generate a fasta
		Write it to fasta file
		"""
		names = self.seq.split(" ")[0]
		seq_name = names.split("_")[1:]
		out_name = names[1:] + ".fasta"
		with open(classA, "r") as data:
			data_list = data.readlines()
			for line in data_list:
				#match the name find correspond sequence
				classA_name = line.split(" ")[0][1:]
				classA_uniport = classA_name.split("_")
				classA_pdb = classA_name.split("_")[0]
				if seq_name == classA_uniport:
					with open(out_name, "w") as out_file:
						out_file.write(self.seq.split(" ")[0]+"\n")
						out_file.write(self.seq.split(" ")[1])
						out_file.write(line.split(" ")[0]+"\n")
						out_file.write(line.split(" ")[1])
					move(out_name, self.fasfold)


class Build_folder():
	"""
	Build a folder
	Need a folder name
	"""
	def __init__(self, foldname):
		self.name = foldname
	def folder(self):
		try:
			os.mkdir(self.name)
		except FileExistsError as e:
			rmtree(self.name)
			os.mkdir(self.name)


def main():
	#Build folder save fasta file
	fasfold = "FASTA_FOLD"
	Fas = Build_folder(fasfold)
	Fas.folder()
	fold_list = os.listdir(fold)
	for f in fold_list:
		path = os.path.join(fold, f)
		if os.path.isfile(path):
			with open(path, "r") as seq:
				ClassTra = Traverse(seq.read(), fasfold)
				ClassTra.write_to_file()
	#Aligment sequence use MAFFT
	for f in os.listdir(fasfold):
		path = os.path.join(fasfold, f)
		#path = path.split(".")[0]
		out = path + ".clw"
		os.system("mafft --localpair --maxiterate 16 --clustalout --inputorder "+path+" > "+out)
	#Build folder save clustalW format file
	clwfold = "CLW_FOLD"
	Clw = Build_folder(clwfold)
	Clw.folder()
	os.system("mv "+fasfold+"/*clw "+clwfold)

if __name__ == "__main__":
	main()
	
