'''
Created on Mar 5, 2014

@author: Gregory Jordan
'''
import logging
import struct

class CVREngine():
	'''
	classdocs
	'''
	filename=""
	ModelName=""
	dict_colors = {}
	
	
	def __init__(self, filename):
		'''
		filename	The CVR file to load.
		'''
		
		## Below is the lookup chart for knowing what value means which directions.	
		"""  This is the view of the model when first loaded in CVRPlay.exe.  Note, 
			because of the camera position X is positive going to the left and z is 
			positive heading away from you.
			   Y
			   |  /z
			   | /
			   |/
		+x---------- (-x)  
			  /|
			 / |
			/  |
		"""	
								##   x, y, z    Approximate hex value   
		self.dict_directions = {'00000':[-1,-1,-1]}	## 00
		self.dict_directions['00001'] = [-1, 0,-1]	## 08
		self.dict_directions['00010'] = [-1,+1,-1]	## 10
		self.dict_directions['00011'] = [ 0,-1,-1]	## 18
		self.dict_directions['00100'] = [ 0, 0,-1]
		self.dict_directions['00101'] = [ 0,+1,-1]	## 28
		self.dict_directions['00110'] = [+1,-1,-1]	## 30
		self.dict_directions['00111'] = [+1, 0,-1]	## 38
		self.dict_directions['01000'] = [+1,+1,-1]	## 40
		self.dict_directions['01001'] = [-1,-1, 0]	## 48
		self.dict_directions['01010'] = [-1, 0, 0]	## 50
		self.dict_directions['01011'] = [-1,+1, 0]	## 58
		self.dict_directions['01100'] = [ 0,-1, 0]	## 60
		self.dict_directions['01101'] = [ 0,+1, 0]	## 68
		self.dict_directions['01110'] = [+1,-1, 0]	## 70
		self.dict_directions['01111'] = [+1, 0, 0]	## 78
		self.dict_directions['10000'] = [+1,+1, 0]	## 80
		self.dict_directions['10001'] = [-1,-1,+1]	## 88
		self.dict_directions['10010'] = [-1, 0,+1]	## 90
		self.dict_directions['10011'] = [-1,+1,+1]	## 98 			
		self.dict_directions['10100'] = [ 0,-1,+1 ]	## A0
		self.dict_directions['10101'] = [ 0, 0,+1 ]	## A8 		
		self.dict_directions['10110'] = [ 0,+1,+1 ]	## B0
		self.dict_directions['10111'] = [+1,-1,+1 ]	## B8
		self.dict_directions['11000'] = [+1, 0,+1]	## C0
		self.dict_directions['11001'] = [+1,+1,+1]	## C8
		self.dict_directions['11010'] = [ 0, 0, 0]	## d0 This appears only at the end of parts sections for direction for some files!  
		## Other files don't have it.	
		
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
		with open(filename,"rb") as f:
			CVRfile = bytearray(f.read())
			logging.info('Opened File')
		pos = 0
	
		# Read "CVR" from file.  Should always be here.
		cvr = struct.unpack("3s", CVRfile[0:3])[0].decode(encoding='UTF-8')		
		if(cvr!="CVR"):  # If this isn't there, then this isn't a CVR file.	
			raise Exception("Not a CVR file: Value was "+ cvr)
		
		
		# How many bytes are there in this file?
		intNumberofbytes = struct.unpack("I", CVRfile[4:8])[0]
		# Check it to see if they are the same or not
		if(intNumberofbytes==len(CVRfile)):
			logging.debug("Number of bytes in file" + str(intNumberofbytes))
		else:
			logging.warning("Number of bytes in file (" + str(len(CVRfile)) + ") does not equals the number of bytes the file thinks it has!"+str(intNumberofbytes))
		
		
		pos = self.findnextcodepos(pos,CVRfile,[0x00,0x00,0x00,0x02])
		
		# Ok first we need to get the length of the object name
		dist = struct.unpack("I", CVRfile[pos:pos + 4])[0]-8
		logging.debug(dist)
		s = str(dist)+"s"  # Then create a filter for unpacking based on it
		
		pos = pos + 4
		
		# The name of the model the file was converted from.
		self.ModelName = struct.unpack(s, CVRfile[pos:pos + dist])[0].decode(encoding='UTF-8')
		logging.info(self.ModelName)
		
	
	
		pos = self.findnextcodepos(pos,CVRfile,[0x00,0x00,0x00,0x03])
		
		# Where is the 3d data stored in this file?
		threedlocation = struct.unpack("I", CVRfile[pos:pos+4])[0] + pos - 1
		logging.debug("3d data is at:" + str(threedlocation))
		
		
		# Find the palette name length.
		pos = self.findnextcodepos(pos,CVRfile,[0x00,0x00,0x01,0x01])
		dist = CVRfile[pos]-8 # length of palette name.
		s = str(dist)+"s"
		pos += 4
		
		PaletteName = struct.unpack(s, CVRfile[pos:pos + dist])[0].decode(encoding='UTF-8')
		logging.info(PaletteName)
	
		# Palette dict_colors
		pos+=16
		logging.debug("pallet nums" + str(CVRfile[pos-1]))
		pos=pos + 1 + CVRfile[pos-1]*3  #10 was the right number for ACP which had 145 for its number. 155-145 = 10
		# Color is wrong on select for the knob parts... as well as the drill arm
		# It isn't getting the right colors when it is # 145 or higher
		inttmp = pos + 3*(245-CVRfile[pos-1])  #it won't be reading in the right values for 155-x... yeah.
		colorcount = 0;
		while pos <= inttmp:
			self.dict_colors[colorcount] = str(CVRfile[pos]) + "," + str(CVRfile[pos+1]) +"," + str(CVRfile[pos+2])
			logging.debug("Color " + str(colorcount)+ ": " + self.dict_colors[colorcount] + ": "  + colorname((CVRfile[pos], CVRfile[pos+1], CVRfile[pos+2])))	
			colorcount+=1
			pos+=3
			
		# TODO: Have someone figure out where the other palette color codes are stored.
		
		
		# Then there is a bunch of stuff I don't know what it does.... O.o
		# So.... lets skip it.
		
		# -----------------------------------------------------------------
		
		# Body Parts 3D data
		# 
		pos = threedlocation
		if CVRfile[threedlocation] == 4:  # Yeah, a 1/256 chance that I'm off by one. 
			# TODO: Should make it check a few more bytes...
			logging.debug("Ok, we're likely at the right location.")
		else:
			#terminate
			raise Exception("Not at the right location!")
		
		#No clue about the number in between here means
		#skip for now
		
	
		# Name length....
		pos = self.self.findnextcodepos(pos,CVRfile,[0x00,0x00,0x01,0x04])
		intNameLength = struct.unpack("I", CVRfile[pos:pos + 4])[0]-8
		
		pos+=4
		# And name
		s = str(intNameLength)+"s"
		AnotherName = struct.unpack(s, CVRfile[pos:pos + intNameLength])[0].decode(encoding='UTF-8')
		logging.info(AnotherName)
		output.write(AnotherName)
		output.write("\n")
		#increment the pos
		pos+=intNameLength
	
		
		
		pos = self.self.findnextcodepos(pos,CVRfile,[0x00,0x02,0x04,0x0C])
		## 00 02 04 0C 00 00 00 nn nn ?? ?? <- nn nn ?? ?? is the number of parts in this object	
		int_numberofparts = struct.unpack("I", CVRfile[pos+3:pos + 7])[0]
		logging.info("Number of parts is " + str(int_numberofparts))
		
		
		## 00 03 04 0C 00 00 00 nn nn nn nn 	< nn of frames
		pos = self.self.findnextcodepos(pos,CVRfile,[0x00,0x03,0x04,0x0C])
		int_number_of_frames = struct.unpack("I", CVRfile[pos+3:pos + 7])[0]
		logging.info("Number of frames is " + str(int_number_of_frames))
	
		
		# lets get the current part's name
		#00 01 04 04	
		pos = self.self.findnextcodepos(pos,CVRfile,[0x00,0x01,0x04,0x04])
		partnameLength = CVRfile[pos]-8	
		logging.debug("Part name length: " + str(partnameLength))  # for srb the value should be 3
		s = str(partnameLength)+"s"
		pos+=4
		AnotherName = struct.unpack(s, CVRfile[pos:pos + partnameLength])[0].decode(encoding='UTF-8')
		logging.info(AnotherName)
		output.write(AnotherName)
		output.write("\n")
		pos+=partnameLength
		
		
		
		# Grab the next parts location!   This will fail curently!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		# TODO, place into a try catch statement as it will fail for some files.
		## I should probably make this throw an error if it isn't correct.	
		pos = self.self.findnextcodepos(pos,CVRfile,[0x00,0x02,0x04,0x04])
		nextpart = struct.unpack("I", CVRfile[pos:pos+4])[0]+pos
		logging.info("Location of next part is " + str(nextpart))
		
		
		
		## There is another distance code here.... not sure why  Not bothering to read it in right now
		
		
		pos = self.findnextcodepos(pos,CVRfile,[0x01,0x02,0x04,0x04])
		
		## TODO use id code movement stuff.
		## Does some scalling here.  As far as I can tell.  It will only use one of these.
		int_scale_z = CVRfile[pos+1+24]
		int_scale_x = CVRfile[pos+3+24]
		int_scale_y = CVRfile[pos+5+24]
	
		# Since the code currently does nothing with these, and the potential of this being important, lets throw a warning if they
		# Don't equal 0
		if(int_scale_z + int_scale_x + int_scale_y != 0):
			logging.warning("Scales z:" + str(int_scale_z) + "  Scales x:" + str(int_scale_x) + "  Scales y:"+ str(int_scale_y))
			logging.warning("Non-zero scaling factor on file!")
		else:
			logging.debug("Scales z:" + str(int_scale_z) + "  Scales x:" + str(int_scale_x) + "  Scales y:"+ str(int_scale_y))
		
		# I'm not sure what these are for.  It affected the view of the object.  Might be length of the stuff.
		# Length?  Perhaps?  Need to see if they match up with anything.
		int_view_z = CVRfile[pos+24]
		int_view_x = CVRfile[pos+2+24]
		int_view_y = CVRfile[pos+4+24]
		logging.info("What? z:" + str(int_view_z) + "  x:" + str(int_view_x) + "  y:"+ str(int_view_y))
	
		
		## Positional data!  
		z0 = struct.unpack("h", CVRfile[pos+30:pos+32])[0]
		x0 = struct.unpack("h", CVRfile[pos+32:pos+34])[0]
		y0 = struct.unpack("h", CVRfile[pos+34:pos+36])[0]
		logging.debug("Position 0 Z: " + str(z0) + "  x:" + str(x0) + "  y:"+ str(y0))
		
		
		## and then we have the rotation point data of the object	
		zr = struct.unpack("h", CVRfile[pos+36:pos+38])[0]
		xr = struct.unpack("h", CVRfile[pos+38:pos+40])[0]
		yr = struct.unpack("h", CVRfile[pos+40:pos+42])[0]
		logging.info("Rotation Point or Offset? Info Z: " + str(zr) + "  x:" + str(xr) + "  y:"+ str(yr))
		
		
		pos+=42
		# Total Number of voxels
		int_totalvox =  struct.unpack("I", CVRfile[pos:pos+4])[0]
		logging.info("Total Voxels count " + str(int_totalvox))
		output.write(str(int_totalvox)+"\n")
		
		pos+=4
		
		
		
		
	
		
		# Ok.  First thing first.  Is this a multipart mesh or not?  I think it is never the case for multi-part objects, but I could be wrong....
		# The problem is some meshes have it, others don't....
		# The method I use below to figure it out probably isn't right, but hopefully it will work.
		# The idea:  If it is a multimesh, this first one always? has 00 00 00 00 before the 3d data, 
		# I check to see if there is 4 0x00 at that location, if there is, then it is a multimesh.   
		bool_multimesh = CVRfile[pos+28]==0 and CVRfile[pos+29]==0 and CVRfile[pos+30]==0 and CVRfile[pos+31]==0
		logging.info("MultiMesh?: " + str(bool_multimesh))
		
		
		if(bool_multimesh):
			#TODO: make this code neater, remove duplication.  God this is ugly here.
			z1 = struct.unpack("h", CVRfile[pos:pos+2])[0]
			x1 = struct.unpack("h", CVRfile[pos+2:pos+4])[0]
			y1 = struct.unpack("h", CVRfile[pos+4:pos+6])[0]
			logging.info("Pos1," + str(x1) + "," + str(y1) + "," + str(z1))
	
			
			#Bunch of stuff inbetween that I think deals with the viewing area.
			#Not really sure.
			#lets... skip it, shall we?
			pos+= 18
			
			z2 = struct.unpack("h", CVRfile[pos:pos+2])[0]
			x2 = struct.unpack("h", CVRfile[pos+2:pos+4])[0]
			y2 = struct.unpack("h", CVRfile[pos+4:pos+6])[0]
		
			logging.info("Pos2," + str(x2) + "," + str(y2) + "," + str(z2))
		
			
			# Now read how many voxels until the next jump
			pos+=6
			vox_count_section = struct.unpack("I", CVRfile[pos:pos+4])[0]
			logging.info("Voxels to next mesh" + str(vox_count_section))
			
			pos+=8
			
			# Yeah.... not sure if this is correct... 
			array_pos = [x1+x2,y1+y2,z1+z2]
			
		else:
			array_pos = [x0,y0,z0]
			vox_count_section = int_totalvox
		
		
		logging.info(array_pos)
		int_tmpcount1 = 0
		int_tmpcount2 = 0
		
		while int_tmpcount1 < int_totalvox:
			print("looped")
			
			while int_tmpcount2 < vox_count_section:	
				
				#print(int_tmpcount)
				#print(pos)
				if('11010' == bytetobinary(CVRfile[pos])[0:5]):
					logging.info("Here it is again")  # didn't find any! on ACP00... but on ones that have multimesh conversions into a single part... its there
					# ok, 
				else:
					
					array_pos[0] = array_pos[0] + dict_directions[bytetobinary(CVRfile[pos])[0:5]][0]
					array_pos[1] = array_pos[1] + dict_directions[bytetobinary(CVRfile[pos])[0:5]][1]
					array_pos[2] = array_pos[2] + dict_directions[bytetobinary(CVRfile[pos])[0:5]][2]
					
					
					
					output.write(str(array_pos[0]) + "," + str(array_pos[1]) + "," + str( array_pos[2]) +"," + dict_colors[CVRfile[pos+2]])  #bytetobinary(CVRfile[pos])[-3:] + "," + str(CVRfile[pos+1]) + "," 
					
					# Really crappy normals
					if(CVRfile[pos+2]>235):
						logging.debug(str(CVRfile[pos+2]) +":"+ dict_colors[CVRfile[pos+2]])
					
					tmparray = [abs(array_pos[0]),abs(array_pos[1]),abs(array_pos[2])]
					output.write("," + str(array_pos[0]) + "," + str(array_pos[1]) + "," + str( array_pos[2]))
					output.write("\n")
					
				pos+=3
				int_tmpcount2+=1
				int_tmpcount1+=1
				
				
			if(bool_multimesh):
				z1 = struct.unpack("h", CVRfile[pos:pos+2])[0]
				x1 = struct.unpack("h", CVRfile[pos+2:pos+4])[0]
				y1 = struct.unpack("h", CVRfile[pos+4:pos+6])[0]
				logging.info("Pos1," + str(x1) + "," + str(y1) + "," + str(z1))
				#Bunch of stuff inbetween that I think deals with the viewing area.
				#Not really sure.
				#lets... skip it, shall we?
				pos+= 18
				
				z2 = struct.unpack("h", CVRfile[pos:pos+2])[0]
				x2 = struct.unpack("h", CVRfile[pos+2:pos+4])[0]
				y2 = struct.unpack("h", CVRfile[pos+4:pos+6])[0]
			
				logging.info("Pos2," + str(x2) + "," + str(y2) + "," + str(z2))
			
				
				# Now read how many voxels until the next jump
				pos+=6
				vox_count_section = struct.unpack("I", CVRfile[pos:pos+4])[0]
				logging.info("Voxels to next mesh" + str(vox_count_section))
				
				pos+=8
				
				# Yeah.... not sure if this is correct... 
				array_pos = [x1+x2,y1+y2,z1+z2]
				int_tmpcount2=0
			
	
		
			