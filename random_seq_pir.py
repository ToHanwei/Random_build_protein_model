#!/usr/bin/python

"""
generate a pir file
those sequences from classA
random select some sequences less 5
"""
import numpy as np

def write_to_file(line, style):
	name, sequence = line.split(" ")
	name = name.split("_")[0][1:]
	if style == "query":
		header = "sequence:{0}:.:.:.:.::::".format(name)
	else:
		header = "structureX:{0}:.:.:.:.::::".format(name)
	name = ">P1;" + name
	sequence = sequence.rstrip() + "*"
	seq_out.write(name+"\n"+header+"\n"+sequence+"\n")

#print("""
#\033[0;31;40m
#####################################
##        Input sequence file       #
#####################################\033[0m
#""")
#seq_file = input()
seq_file = "classA_pdb_seq.txt"

seq = open(seq_file, mode="r")
seq_list = seq.readlines()
seq_query, seq_templat = seq_list[0], seq_list[1:]
seq_out = open("modeller_sequences.pir", mode="w")

#select 5 random number as index
length = len(seq_templat)
a = np.random.randint(0, length, 5)
rand = list(set(a))

#write query sequence to seq_out
write_to_file(seq_query, "query")

#write templat sequence to seq_out
for i in rand:
	select_seq = seq_templat[i]
	name = write_to_file(select_seq, "templect")

seq.close()
seq_out.close()
