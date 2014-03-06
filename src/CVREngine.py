'''
Created on Mar 5, 2014

@author: Gregory Jordan
'''
import logging

class CVREngine():
	'''
	classdocs
	'''
	filename=""

	def __init__(self, filename):
		'''
		filename	The CVR file to load.
		'''
		self.filename = filename
	
	def findnextcodepos(self, start_pos, filebytes, lookupcode):
		'''
		start_pos	Where to start the search from.
		filebytes	The array of bytes that we are searching in.
		lookupcode	Should be  4 hex values.  Example [0x00,0x00,0x00,0x02]
		Return		Will return -1 if code is not found further on in file.  Otherwise the position right after the label.  
		'''
		#ok, lets do things properly for this
		#the lookupcode 
		# 
		if(len(lookupcode)!=4):
			raise Exception("Improper lookupcode length")
		
		# filebytes is a bytearray
		# start_pos is the position the user wants to start at.
		answer = filebytes.index(bytearray((lookupcode[0],lookupcode[1],lookupcode[2],lookupcode[3])),start_pos)+4
		logging.debug("Found " + str(lookupcode)+ " returning position: " + str(answer))
		return answer
		
	def load(self, filename):
		print("Blah")
		

	
		