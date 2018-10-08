#coding:utf-8

__author__ = "Wei"
__maill__ = "hanwei@shanghaitech.edu.cn"
__time__ = "2018-10-8"

from temp import SCORE_VAR
from os import rename
from os import system
from sys import argv
from sys import version_info
from shutil import move
from datetime import datetime 
from modeller import *              
from modeller.automodel import *  

class MyModel(automodel):
	"""
	Add resduce type
	"""
	def special_patches(self, aln):
		self.patch(residue_type='DISU', residues=(self.residues['99'], self.residues['190']))

def Analysis_text(pirfile):
	"""
	Analysis the input pir file, to get pdb name
	Return pab name as a list
	"""
	pdb = []
	pir = open(pirfile, mode="r")
	pir_list = pir.readlines()
	pir_list = pir_list[3:]
	for i in range(len(pir_list)):
		if i%3 == 0:
			pdb_name = pir_list[i].split(";")[1].rstrip()
			#pdb_name = "./ClassA_template_pdb/" + pdb_name
			pdb.append(pdb_name)
	return(pdb)


def Build_model(pir, pdb, query):
	"""
	Build model, use modeller
	"""
	log.verbose()    
	env = environ()  
	# directories for input atom files
	env.io.atom_files_directory = ['.', './PDB_MM_CLEAR/']
	model = MyModel(env,
	            alnfile  = pir,						 # alignment filename
	            knowns   = pdb,                      # codes of the templates
	            sequence = query,                    # code of the target
		    assess_methods=(assess.DOPE, assess.GA341))
	model.starting_model= 1
	model.ending_model  = 100
	model.make()
	return model


def Select_model(model):
	"""
	Select the highest dope score model in this loop
	Note that dope score is negative number
	"""
	# Get a list of all successfully built models from a.outputs
	Models = [x for x in model.outputs if x['failure'] is None]
	# Rank the models by DOPE score
	key = 'DOPE score'
	if version_info[:2] == (2,3):
	    # Python 2.3's sort doesn't have a 'key' argument
	    Models.sort(lambda a,b: cmp(a[key], b[key]))
	else:
	    Models.sort(key=lambda a: a[key])
	# Get top model
	best_model = Models[0]
	best_score = best_model[key]
	best_name = best_model["name"]
	return(best_name, best_score)


def Write_log(name, score, pdb):
	"""
	Move higst DOPE score to Best_model folder
	Write information to log file
	"""
	COUNT = argv[1]							#cycle index
	times = datetime.now()					#the point at which the script runs
	date = times.strftime("%Y-%m-%d")		#record data
	time = times.strftime("%H:%M:%S")		#record time point
	new_name = date + "_" + time + ".pdb"	#best model new name
	rename(name, new_name)
	best = open("Best_model.log", mode="a")
	detaile="UPDATE INFORMATION\nDATE:\t{0}\nTIME:\t{1}\n".format(date, time)
	best.write(detaile)
	model_infor = "MODEL:\t{0}\nSCORE:\t{1}(DOPE)\n".format(new_name, score)
	best.write(model_infor)
	model_template = "TEMPLATE:\t"+str(pdb) + "\n"
	best.write(model_template)
	#update times
	best.write("UPDATE:\t{0}\n".format(COUNT))
	#all model number
	best.write("SUM:\t{0}\n".format(int(COUNT)*100))
	best.write("#"*55+"\n\n")
	move(new_name, "./Best_model")
	best.close()


def main():
	#Import some necessary files
	query = "o5an1"
	pir = "modeller_sequences.pir"
	pdb = tuple(Analysis_text(pir))
	#Function, to build the model
	model = Build_model(pir, pdb, query)
	best_name, best_score = Select_model(model)
	if float(best_score) <= float(SCORE_VAR):
		Write_log(best_name, best_score, pdb)	
		with open('temp.py', 'w') as temp:
			temp.write('SCORE_VAR='+str(best_score))
	system("rm "+query+"*")

if __name__ == "__main__":
	main()

