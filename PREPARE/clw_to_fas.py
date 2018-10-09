#!/usr/bin/python3
#codeing:utf-8

from sys import argv
from os import remove
from os import listdir
from os.path import isfile
from os.path import exists
from collections import defaultdict

#Fasta format files folder
#fold = argv[1]
#fold = "./PDB_MM_sequence"
fold = "./CLW_FOLD"
#ClassA sequences
#classA = argv[2]
classA = "./classA_data.txt"
outname = "./classA_pdb_seq.txt"

def Analyse_classa_data(classA):
	classA_dict = defaultdict(str)
	classA_file = open(classA, mode="r")
	classA_data = classA_file.readlines()
	for line in classA_data:
		line_list = line.split(" ")
		classA_dict[line_list[0]] = line_list[1].rstrip()
	return(classA_dict)


def Write_to_file(seq_list):
	outfile = open(outname, mode="a")
	for seq in seq_list:
		outfile.write(seq)
	outfile.write("\n")
	outfile.close()


def Analyse_clw_fold(fold, classA):
	classA_dict = Analyse_classa_data(classA)
	for clw in  listdir(fold):
		clw = fold + "/" + clw
		sequ = defaultdict(str)
		if isfile(clw):
			clwfile = open(clw, mode="r")
			clwlines = clwfile.readlines()[3:]
			for line in clwlines:
				line_list = line.split(" ")
				if line_list[0] not in ["", "\n"]:
					while "" in line_list:
						line_list.remove("")
					sequ[line_list[0]] += line_list[1].rstrip()
			classA_seq = []
			#other_seq, classA_seq = [], []
			for key in sequ.keys():
				ke = ">" + key
				if ke in classA_dict.keys():
					classA_seq = list(classA_dict[ke])
					other_seq = list(sequ[key])
				else:
					pdb_seq = list(sequ[key])
					with open(outname, "a") as outfile:
						outfile.write(">"+key+" ")
			j, flag = 0, "GO"
			for i in range(len(other_seq)):
				while classA_seq[j]!=other_seq[i]:
					if other_seq[i] == "-":
						flag = "STOP"
						break
					else:
						pdb_seq.insert(j, classA_seq[j])
						j += 1
				if flag == "STOP":
					flag = "GO"
				else:
					j += 1
			try:
				pdb_seq+=classA_seq[j:]
			except IndexError as e:
				pass
			Write_to_file(pdb_seq)
			clwfile.close()


if __name__ == "__main__":
	if exists(outname): remove(outname)
	Analyse_clw_fold(fold, classA)

