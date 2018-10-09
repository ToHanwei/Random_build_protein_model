# --*-- coding:utf-8 --*--

detail = '''
========================================================
+        Download Fasta format file from pdbID         +
+   Recept a txt format file with pdbID line by line   +
========================================================
'''

__author__ = 'Wei'
__date__ = '2018-07-25'
__mail__ = 'hanwei@shanghaitech.edu.cn'


import os
from urllib import request

print(detail)
filee = input('Place input you txt format file: ')
pdbID = open(filee, 'r')

try:
	os.mkdir('Download_PDB')
except FileExistsError as e:
	pass
finally:
	pdb_list = os.listdir('Download_PDB')
	os.chdir('Download_PDB')

for id in pdbID:
	url1 = "https://files.rcsb.org/view/"
	id = id.strip()
	if id+".pdb" in pdb_list:
		print(id+".pdb"+" already existed!")
		continue
	url = url1 + id + ".pdb"
	html = request.Request(url)
	page = request.urlopen(html).read()
	page = page.decode('utf-8')
	files = open(id+'.pdb', 'w')
	files.write(page)
	print('%s has download!!!' % id)
	files.close()

pdbID.close()
