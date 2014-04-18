#! /usr/bin/python

"""
Help on module makeRefOmesDB:

NAME
	makeRefOmesDB - making reference proteome and genome for functional analysis.

FILE
	~/myRepos/funcSUMO/makeRefOmesDB.py

DESCRIPTION
	More description.

DEPENDENCIES

"""

def makeRefOmesDB(UniprotRefProtFasta="", UniprotG2acc="", outputDB=""):

	# os for checking eligibility of files
	import os
	# sqlite3 for making sqlite databse
	import sqlite3
	# SeqIO in Biopython for parsing FASTA file
	from Bio import SeqIO

	# If function called without valid arg value, ask for them
	if UniprotRefProtFasta == "":
		UniprotRefProtFasta = raw_input("Please specify the absolute path for reference proteome FASTA file:")

	if UniprotG2acc == "":
		UniprotG2acc = raw_input("Please specify the absolute path for gene-protein accociation (.gene2acc) file:")

	#if UniprotIdmap == "":
	#	UniprotIdmap = raw_input("Please specify the absolute path for id mapping (.idmapping) file:")

	if outputDB == "":
		outputDB = raw_input("Please specify the name for output database (.sqlite will be added automatically)") + ".sqlite"

	# Check if those files are there
	if not (os.path.exists(UniprotRefProtFasta) & os.path.exists(UniprotG2acc)):
		print("Not all file names are valid.")
		exit()

	# Get data from files.
	print("Extracting protein data from fasta...")
	faParser = SeqIO.parse(UniprotRefProtFasta, "fasta")
	intoRefProt = [(record.id.split("|")[1], len(record),\
			record.seq, record.description) \
			for record in faParser]
	
	print("Extracting gene protein association from g2acc...")
	with open(UniprotG2acc) as g2acc:
		intoG2acc = g2acc.readlines()
	intoG2acc = [(line.split(" ")[1], line.split(" ")[2]) \
			for line in intoG2acc]

	conn = sqlite.connect(outputDB)
	c = conn.cursor()
	# Make reference proteome table, g2acc table
	createProt_G2accTablesStmt = "CREATE TABLE IF NOT EXIST refProt \
	 (pid INT AUTOINCREMENT PRIMARY KEY, \
	 UniprotAC_refProt VARCHAR UNIQUE, plength INT, \
	 aaSeq TEXT, \
	 pdescription VARCHAR); \
	CREATE TABLE IF NOT EXIST G2acc \
	 (accid INT AUTOINCREMENT PRIMARY KEY, \
	 ENSG_G2acc VARCHAR, \
	 UniprotAC_G2acc VARCHAR UNIQUE);"
	# Make gene-protein association table
