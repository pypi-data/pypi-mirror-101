#!/usr/bin/env python

import os
import glob
import subprocess
from runmonitor import stat_tools as stt

def check_error(rd=None):
	linelist = get_linelist(rd)
	error_file = linelist[7].split()[5].strip()
	return error_file

def get_job_id(rd=None):
	linelist = get_linelist(rd)

	job_id = linelist[7].split()[5].split(".")[0].strip("(").strip()
	print(job_id)
	return job_id

def get_linelist(rd=None,num_errors=1):
	"""
	Inputs:
	---------
	rd = rundir, if not given will default to cwd
	num_errors = number of individual failed job lines to return; each failed job consists of 10 lines. 
	These are started from the top of the list, assuming failures will occur for homogeneous reasons
	If the value passed for num_errors is not an int it will return all of the failures instead

	Outputs:
	----------
	A list containing the lines of the first num_errors error messages in the .dagman.out

	"""
	#setup
	linelist = []
	if (rd == None):
		rd = os.getcwd()

	#generalized against non-standard dag names
	dag_prefix, _ = stt.determine_dag_prefix_and_run_status(rd)
	dagman = open(os.path.join(rd,dag_prefix+".dag.dagman.out"))
	dag_list = dagman.readlines()[::-1]
	dagman.close()

	#count back till we find the start of the rror messages
	for line in dag_list:
		linelist.append(line)
		if ("ERROR: the following job(s) failed" in line):
			break
	#order front to back
	linelist = linelist[::-1]
	#each error code is 10 lines long, so if num_errors is an int this will get you num_errors number of error codes
	if type(num_errors) == int:
		linelist = linelist[1:10*num_errors+2]
	else: # if num_errors is not an error code, this will go till it finds the end of the error codes, then cut linelist there
		linelist = linelist[1:]
		for j,line in linelist:
			if "<END>" in line: #<END> appears in the last separator of the error codes
				linelist = linelist[:j]
				break
	return linelist

def check_effective_samples_error(iteration,rd=None):
	import glob
	import sys

	if rd == None:
		rd = os.getcwd()

	filename = glob.glob(rd+"/iteration_" + str(iteration) + "_cip/logs/cip*.err")[0]
	err = open(filename)
	err_lines = err.readlines()
	err.close()

	for item in err_lines[::-1]:
        	if ("Effective samples = nan" in item):
                	print(True)
                	return True
	print(False)
	return False

def get_ile_job(rd=None):
	check_error(rd)

def identify_slot(process_id):
	cmd = ["condor_history",process_id,"-limit","1","-af","LastRemoteHost"] #command courtesy of James Clark
	histpipe = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	out,err = histpipe.communicate()
	return out


def check_encodings_error(rd=None,check_node=False):
	import sys
	
	if rd == None:
		rd = os.getcwd()
             
	error_list = get_linelist(rd,5)
	failids = []
	for i,line in enumerate(error_list):
		# return val -6 = encodings error (it seems? I don't know where that would be coded)
		if "Node return val: -6" in line:
			# The next line has, e.g.:  12/06/20 15:06:05           Error: Job proc (67422388.0.0) failed with status 35
			idline = error_list[i+1]
			failid = idline.split("(")[1].split(")")[0] # hacky string parsing, assuming no other parentheses
			failids += [failid]

	if check_node and failids != []:
		failslots = []
		for root, dirs, files in os.walk(rd,topdown=True,followlinks=True):
			for name in files:
				for failid in failids:
					if failid in name:
						err = open(os.path.join(root,name))
						err_lines = err.readlines()
						err.close()

						for item in err_lines[::-1]:
							if ("No module named 'encodings'" in item):
								process = fname.split(".")[0].split("-")[-1]
								failslots += [identify_slot(failid,process)]
								continue
		print(failslots)
		return True
	elif failids != []:
		return True
	else:
		return False




	""" filenames = glob.glob(rd+"/iteration_" + str(iteration) + "_ile/logs/ILE*" + str(job_id) + "*.err")

	for fname in filenames:
		err = open(fname)
		err_lines = err.readlines()
		err.close()

		for item in err_lines[::-1]:
			if ("No module named 'encodings'" in item):
				print(True)
				if check_node:
					process = fname.split(".")[0].split("-")[-1]
					print(identify_slot(job_id,process))
				return True
	print(False)
	return False """

#add_req(rd,slot)

def identify_gpu_config_fail(rd=None):
	if rd == None:
		rd = os.getcwd()

	#get some representative errors
	#5 is just a random value; the issue is that usually virtually all of the fails will be because of a single blackhole
	#this way we have a chance to catch more; one could do all of them but condor_history is a slow command
	#after a bit of testing, this works pretty well
	error_list = get_linelist(rd,5)
	gpu_fail_ids = []
	gpu_fail_slots = []

	for i,line in enumerate(error_list):
		# return val 35 = no cupy error
		if "Node return val: 35" in line:
			# The next line has, e.g.:  12/06/20 15:06:05           Error: Job proc (67422388.0.0) failed with status 35
			idline = error_list[i+1]
			failid = idline.split("(")[1].split(")")[0] # hacky string parsing, assuming no other parentheses
			gpu_fail_ids += [failid]

	for failid in gpu_fail_ids:
		failslot = identify_slot(failid)# see above
		if failslot not in gpu_fail_slots:
			gpu_fail_slots += [failslot]

	return gpu_fail_slots

def check_frequency_error(iteration,job_id,rd=None):
	import glob
	import sys

	if rd == None:
		rd = os.getcwd()

	filename = glob.glob(rd+"/iteration_" + str(iteration) + "_ile/logs/ILE*" + str(job_id) + "*.err")[0]
	err = open(filename)
	err_lines = err.readlines()
	err.close()

	for item in err_lines[::-1]:
        	if ("Initial frequency is too high" in item):
                	print(True)
                	return True
	print(False)
	return False

def check_mc_range_error(rd=None):
	import glob
	import sys

	if rd == None:
		rd = os.getcwd()

	filename = glob.glob(rd+"/iteration_" + str(iteration) + "_cip/logs/cip*.err")[0]
	err = open(filename)
	err_lines = err.readlines()
	err.close()

	for item in err_lines[::-1]:
        	if not ("Points used in fit" in item):
                	print(True)
                	return True
	print(False)
	return False

