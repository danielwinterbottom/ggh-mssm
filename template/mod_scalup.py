"""
Script opens LHE file and replaces SCALUP for remnant events with
the provided 'hdamp' value
Discussed here (p. 8): https://link.springer.com/content/pdf/10.1007/JHEP01(2016)056.pdf 
"""
import numpy as np
import os, sys

lhe_in = sys.argv[1]
lhe_out = lhe_in[:-4] + "_mod.lhe"
hdamp = float(sys.argv[2])

event_index = -9999
scalup = []
with open(lhe_in, "r") as infile:
	with open(lhe_out + "_tmp", "w") as outfile:
		for i, row in enumerate(infile):
			#if i>200:
			# 	break
			if "<event>" in row:
				pTH = hdamp	# if pTH cannot be read from lhe (should never be the case)
				event_index = i
				outfile.write(row)

			elif i == event_index+1:
				toprow = [j.strip() for j in row.split(" ") if j != ""]
				scalup.append(float(toprow[3]))
				toprow[3] = "SCALUP"
				toprow = "      " + " ".join(map(str, toprow)) + "\n"
				#print toprow
				outfile.write(toprow)

			elif i == event_index+4:
				outfile.write(row)
				row = [float(j.strip()) for j in row.split(" ") if j != ""]
				if row[0] == 25 or row[0] == 35 or row == 36:
					px = row[7]
					py = row[8]
					pTH = np.sqrt(px**2 + py**2)

			elif "#rwgt" in row:
				outfile.write(row)
				row = [j.strip() for j in row.split(" ") if j != ""]
				if row[1] in ["2", "3"]:	# select remnant events
					scalup[-1] = np.min([pTH, hdamp])

			else:
				outfile.write(row)

c = 0
with open(lhe_out + "_tmp", "r") as infile:
	with open(lhe_out, "w") as outfile:
		for row in infile:
			if "SCALUP" in row:
				outfile.write(row.replace("SCALUP", "{:.5E}".format(scalup[c])))
				c += 1
			else:
				outfile.write(row)

os.system("rm {}_tmp".format(lhe_out))
