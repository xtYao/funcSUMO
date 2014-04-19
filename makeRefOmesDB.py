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
	intoRefProt = [(record.name.split("|")[1], int(len(record)),\
			str(record.seq), str(record.description)) \
			for record in faParser]
	
	print("Extracting gene protein association from g2acc...")
	with open(UniprotG2acc) as g2acc:
		linesG2acc = g2acc.readlines()
	intoG2acc = [(line.split("\t")[0], line.split("\t")[1]) \
			for line in linesG2acc]

	conn = sqlite.connect(outputDB)
	c = conn.cursor()
	# Make reference proteome table, g2acc table
	createProt_G2accTablesStmt = "CREATE TABLE IF NOT EXISTS refProt \
	 (pid INTEGER PRIMARY KEY AUTOINCREMENT, \
	 UniprotAC_refProt VARCHAR UNIQUE, \
	 plength INTEGER, \
	 aaSeq TEXT, \
	 pdescription VARCHAR); \
	CREATE TABLE IF NOT EXISTS G2acc \
	 (g2accid INTEGER PRIMARY KEY AUTOINCREMENT, \
	 ENSG_G2acc VARCHAR, \
	 UniprotAC_G2acc VARCHAR UNIQUE);"
	
	c.executescript(createProt_G2accTablesStmt)
	c.executemany("INSERT INTO refProt \
	(UniprotAC_refProt, plength, aaSeq, pdescription) \
	VALUES (?,?,?,?)", intoRefProt)
	c.executemany("INSERT INTO G2acc \
	(ENSG_G2acc, UniprotAC_G2acc) VALUES (?,?)", intoG2acc)
	
	conn.commit()
	conn.close()
	
