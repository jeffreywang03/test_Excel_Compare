import csv, os
import time
import re
from datetime import datetime
from tkinter import *
from tkinter import filedialog

def excelCompare(filename1, filename2):

	print("")
	print("")	
	print("---------------------FILE PATHS FOR THE TWO CSV FILES:-------------------------")
	print("Filename 1: "+filename1)
	print("Filename 2: "+filename2)

	csvFile1 = open(filename1)
	csvReader1 = csv.reader(csvFile1)
	csvData1 = list(csvReader1)

	csvFile2 = open(filename2)
	csvReader2 = csv.reader(csvFile2)
	csvData2 = list(csvReader2)	

	print("\n===============================================================================")
	print("----------------------------------BEGIN TEST-----------------------------------")

	counter = 0
	error_count = []

	pass_counter = 0
	fail_counter = 0
	error_list = []

	#CHECK IF FILES HAVE THE SAME AMOUNT OF DATA
	if len(csvData1) != len(csvData2):
		print("\nSCRIPT END: The two files have different amount of data - check for missing data!")
		print("Lines in File 1: %i" % len(csvData1))
		print("Lines in File 2: %i" % len(csvData2))
		print("\n===============================================================================")		
		#Terminate script if different amount of data - check manually
		exit() 

	#VERIFICATION OF DATA
	for line in csvData1:


		#If the rows match identically
		if csvData1[counter] == csvData2[counter]: #csvData1[counter] = data of entire row
			pass_counter +=1
			#print("Line: "+str(counter+1)+" - PASS")

		#Else identify mismatches and identify any false failures due to formatting/puncutations
		else:
			diff = set(csvData1[counter])^set(csvData2[counter])
			#append differences from the two files into one list called diff_list
			diff_list = list(diff)

			#clean up all punctuation that are not letters or numbers to prevent false failures
			clean_list=[]
			for i in diff_list:
				a = re.sub('[^A-Za-z0-9]+','', i)
				b = a.lower()
				clean_list.append(b)
				#remove any empty entries
				if '' in clean_list:
					clean_list.remove('')

			#VERIFICATION - One Column of mismatch
			if len(clean_list)==2:
				if clean_list[0]==clean_list[1]:
						pass_counter +=1
				else:
					print("Line: "+str(counter+1)+" - FAIL")
					print(diff_list)
					error_list.append(counter+1)
					fail_counter += 1				
			#VERIFICATION - Two Columns of mismatch		
			elif len(clean_list)==4:
				if clean_list[0]==clean_list[1] or clean_list[0]==clean_list[2] or clean_list[0]==clean_list[3]:
						pass_counter +=1
				elif clean_list[1]==clean_list[0] or clean_list[1]==clean_list[2] or clean_list[1]==clean_list[3]:
						pass_counter +=1				
				elif clean_list[2]==clean_list[0] or clean_list[2]==clean_list[1] or clean_list[2]==clean_list[3]:
						pass_counter +=1
				elif clean_list[3]==clean_list[0] or clean_list[3]==clean_list[1] or clean_list[3]==clean_list[2]:
						pass_counter +=1
				else:
					print("Line: "+str(counter+1)+" - FAIL")
					print(diff_list)
					error_list.append(counter+1)
					fail_counter += 1
			#VERIFICATION - Less than One Column of mismatch, OR multiple mismatches (greater than Two)									
			else:
				if len(clean_list)<2:
					pass_counter +=1
				else:
					print("Line: "+str(counter+1)+" - FAIL: CHECK ROW FOR INCONSISTENT DATA (Multiple differences in row)")
					print(diff_list)

					print(clean_list)
					error_list.append(counter+1)
					fail_counter += 1

		counter += 1

	print("\n===============================================================================")
	print("--------------------------------------RESULTS----------------------------------\n")
	print("Total Lines Tested: " + str(pass_counter+fail_counter))
	print("PASSED: " + str(pass_counter))
	print("FAILED: " + str(fail_counter))
	if fail_counter>0:
		print("Check lines: ")
		print(error_list)
	print("\n===============================================================================")