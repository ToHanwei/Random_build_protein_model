#!/codeing;utf-8

from argparse import ArgumentParser
from collections import defaultdict

Arg = ArgumentParser()
Arg.add_argument("--name", "-n", help="Input name's file")
arg = Arg.parse_args()

name_dict = defaultdict(str)
with open(arg.name, mode='r') as pdb_names:
	line_names = pdb_names.readlines()
for line in line_names:
	line_list = line.split("_")
	pdb, protein, spec = line_list[0], line_list[1].lower(), line_list[2].lower()
	if len(spec.strip()) > 5:
		spec = spec[:5] + "\n"
	name_dict[pdb] = protein + "_" + spec

name_tuple = sorted(name_dict.items(), key=lambda x:x[0])

with open("classA_sort_name.txt", "a") as outfile:
	for line in name_tuple:
		outfile.write(line[0]+"_"+line[1])

