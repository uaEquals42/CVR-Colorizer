'''
Created on Mar 5, 2014

@author: Gregory Jordan
'''
import logging
import struct


def colorname(color):
	colornames = {(0,0,0):"Black",(255,0,0):"Red",(128,128,0):"Olive",(128,0,128):"Purple",(0,0,128):"Deep Blue",(0,255,255):"Sky Blue"}
	colornames[(255,255,0)] = "Yellow"
	colornames[(85,43,21)] = "Dark brown"
	colornames[(192,208,248)] = "Pale blue"
	colornames[(172,129,81)] = "Light brown"
	colornames[(143,114,82)] = "Brown"
	colornames[(120,98,74)] = "Brown"
	colornames[(54,84,47)] = "Dark green"
	colornames[(30,53,30)] = "Really dark green"
	colornames[(215,183,156)] = "Tan with pink tinge"
	colornames[(182,122,97)] = "Brown with pink tinge"
	colornames[(113,61,49)] = "Brown with pink tinge"
	colornames[(70,36,39)] = "Dark brown with pink tinge"
	colornames[(231,244,231)] = "Light gray with slight blue tinge"
	colornames[(192,212,205)] = "Grayish green"
	colornames[(163,188,185)] = "Gray"
	colornames[(72,88,88)] = "Dark Gray"
	colornames[(27,33,31)] = "Almost black"
	colornames[(143,140,18)] = "Muddy Yellow"
	colornames[(82,66,12)] = "Brown"
	colornames[(52,29,9)] = "Dark reddish brown"
	colornames[(232,84,84)] = "Pale bright red"
	colornames[(248,248,236)] = "White"
	colornames[(255,255,255)] = "White"
	colornames[(244,240,212)] = "Pale yellow"
	colornames[(224,192,96)] = "Brownish yellow"
	colornames[(232,136,8)] = "Orange"
	colornames[(236,92,0)] = "Orange red"
	colornames[(224,44,20)] = "Red"
	colornames[(176,20,20)] = "Dark red"
	colornames[(214,157,106)] = "Tan"
	colornames[(215,184,152)] = "Tan"
	colornames[(172,54,82)] = "Purple red"
	colornames[(76,41,13)] = "Brown"
	colornames[(119,118,40)] = "Olive"
	colornames[(184,192,96)] = "Pale olive"
	colornames[(88,140,44)] = "Green"
	colornames[(132,192,200)] = "Pale blue"
	colornames[(100,168,184)] = "Dark pale blue"
	colornames[(77,156,176)] = "Dark pale blue"
	colornames[(64,115,128)] = "Dark pale blue"
	colornames[(42,101,120)] = "Dark blue"
	colornames[(35,90,110)] = "Dark blue"
	colornames[(17,50,79)] = "Navy"
	colornames[(14,37,75)] = "Navy"
	colornames[(68,32,12)] = "Dark brown"
	colornames[(176,232,188)] = "Pale blue green"
	colornames[(116,192,160)] = "Greenish blue"
	colornames[(60,148,124)] = "Greenish blue"
	colornames[(40,66,61)] = "Very dark greenish blue"
	colornames[(245,200,96)] = "Yellow"
	colornames[(0,97,255)] = "Blue"
	colornames[(191,103,21)] = "Orange-ish brown"
	colornames[(100,16,156)] = "Purple"
	colornames[(219,205,22)] = "Yellow"
	colornames[(0,252,252)] = "Sky blue"
	colornames[(24,184,228)] = "Sky blue"
	colornames[(255,255,255)] = "White"
	
	try:
		colorname = colornames(color)
		return colorname
	except:
		colours = {}
		for key in colornames:
			red, green, blue = key
			mred = abs(red - color[0]) 
			mgeen = abs(green - color[1]) 
			mblue = abs(blue - color[2]) 
			colours[(mred + mgeen + mblue)] = colornames[key]
		return colours[min(colours.keys())]


class VoxelPoint(object):
	''' A simple store of voxel data.  Mostly so that code is easier to understand elsewhere'''	
	def __init__(self, bytepos, location, color, norm1, norm2):
		self.bytepos = bytepos
		self.location = location
		self.color = color
		self.norm1 = norm1
		self.norm2 = norm2
		
		

class Mesh(object):
	''' Contains a list of voxels and other details '''
	meshname = "Mesh "
	__dimensions = None
	currentLocation = None
	voxels = None
	
	
	def __init__(self, Number, startposition):
		self.meshname = self.meshname + str(Number) 
		self.currentLocation = startposition
		self.voxels = []
		self.currentLocation = [0,0,0]  #x, y, z
	
	def paletteCodesinUse(self):
		''' Returns a set of the palette numbers in use for this mesh'''
		colorcodes = set()
		for v in self.voxels:
			colorcodes.add(v.color)
		return colorcodes
	
	def replacecolorcode(self, fromcolor, tocolor):
		# if fromcolor is -1 all colors will be replaced with new value
		if(fromcolor> 255 or tocolor > 255 or tocolor <0 or fromcolor <-1):
			raise Exception("Invalid input for replacecolorcode")
		logging.info("Replacing colors for "+ self.meshname)
		for v in self.voxels:
			if v.color==fromcolor or fromcolor==-1:
				v.color=tocolor	
			
		
	def addvoxel(self,byteposition, xyzDelta, paletteColor, norm1, norm2):
		self.currentLocation[0] += xyzDelta[0]
		self.currentLocation[1] += xyzDelta[1]
		self.currentLocation[2] += xyzDelta[2]
		self.voxels.append(VoxelPoint(byteposition,(self.currentLocation[0],self.currentLocation[1],self.currentLocation[2]), paletteColor, norm1, norm2))
	
	def dimensions(self):
		
		if self.__dimensions == None:
			logging.info("Calculate diminsions")
			xmin = self.voxels[0].location[0]
			xmax = self.voxels[0].location[0]
			ymin = self.voxels[0].location[1]
			ymax = self.voxels[0].location[1]
			zmin = self.voxels[0].location[2]
			zmax = self.voxels[0].location[2]
			for vox in self.voxels:
				if vox.location[0] < xmin:
					xmin = vox.location[0]
				if vox.location[1] < ymin:
					ymin = vox.location[1]
				if vox.location[2] < zmin:
					zmin = vox.location[2]
					
				if vox.location[0] > xmax:
					xmax = vox.location[0]
				if vox.location[1] > ymax:
					ymax = vox.location[1]
				if vox.location[2] > zmax:
					zmax = vox.location[2]
			self.__dimensions = (xmin, xmax, ymin, ymax, zmin, zmax)
		return self.__dimensions
				
				

class CVREngine(object):
	'''
	classdocs
	'''

	
	
	
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
		
		
		
		self.ModelName1=""
		self.ModelName2=""
		self.dict_colors = {}
		self.int_numberofparts = -1     
		self.int_number_of_frames = -1
		self.parts = None  # structure will be as follows  
		#				[["Part Name",[Mesh]], ["Part Name",[Mesh]], etc]
		self.parts = []
		
		self.filename = filename
		self.load(filename)
		logging.info(len(self.parts))
	
	
	def returnMesh(self):
		return self.parts[0][1][0]
		
			
	def bytetobinary(self, byte):
		#Returns a string of length 8 of the byte of data fed to it.
		#Currently doesn't have any sanity checks on the input data.
		# TODO: Create a sanity check for the input.
		stringxx = bin(byte)[2:]
		while len(stringxx)<8:
			stringxx = "0" + stringxx
		return stringxx
	
	def findnextcodepos(self, start_pos, filebytes, lookupcode):
		'''	
		start_pos	Where to start the search from.
		filebytes	The array of bytes that we are searching in.
		lookupcode	Should be  4 hex values.  Example [0x00,0x00,0x00,0x02]
		Return		Will return -1 if code is not found further on in file.  Otherwise the position right after the label.  
		'''
		if(len(lookupcode)!=4):
			raise Exception("Improper lookupcode length")
		
		answer = filebytes.index(bytearray((lookupcode[0],lookupcode[1],lookupcode[2],lookupcode[3])),start_pos)+4
		logging.debug("Found " + str(lookupcode)+ " returning position: " + str(answer))
		return answer

	def replaceAllcolors(self, fromcolor, newcolor):
		for p in self.parts:
			for m in p[1]:
				m.replacecolorcode(fromcolor, newcolor)
		
	def saveColors(self, filename):
		# First we need to get the original filedata that we are going to modify.
		with open(self.filename,"rb") as f:
			CVRfile = bytearray(f.read())
			logging.info('Opened File')
		# Then we will modify the data in the bytearray
		
		# TODO: Write the code for modifing the values
		for p in self.parts:
			for m in p[1]:
				for v in m.voxels:
					CVRfile[v.bytepos+2] = v.color
		
		# Save the modified bytearray to the new filename
		with open(filename,"wb") as output:	
			output.write(CVRfile)
			logging.info("Saved file")
		
	
	def export(self, filename):
		#Saves in a human and machine readable format to the given filename.
		with open(filename,"w") as output:	
			output.write("CVR\n")
			output.write(self.ModelName1+"\n")
			output.write(self.ModelName2+"\n")
			output.write(str(self.int_numberofparts)+"\n")
			for part in self.parts:
				output.write("P," + part[0]+"\n")
				for om in part[1]:
					for v in om.voxels:
						
						output.write("V, "+ str(v.location[0])+ "," + str(v.location[1])+ "," + str(v.location[2]))
						
						if(v.color in self.dict_colors):
							output.write(","+self.dict_colors[(v.color)])
				
						else:
							output.write(","+"255,  0,242")
							# TODO: make the user able to choose or what the color for unknown colors will be.
							logging.warning("Color Code not Known")
						output.write(",0,0,0") # Normals would be here.. if we knew what they are.
						output.write("\n")
				
		
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
		self.ModelName1 = struct.unpack(s, CVRfile[pos:pos + dist])[0].decode(encoding='UTF-8')
		logging.info(self.ModelName1)
		
	
	
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
		logging.debug("palette num" + str(CVRfile[pos-1]))
		pos=pos + 1 + CVRfile[pos-1]*3  #10 was the right number for ACP which had 145 for its number. 155-145 = 10
		# Color is wrong on select for the knob parts... as well as the drill arm
		# It isn't getting the right colors when it is # 145 or higher
		inttmp = pos + 3*(245-CVRfile[pos-1]-1)  #it won't be reading in the right values for 155-x... yeah.
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
		pos = self.findnextcodepos(pos,CVRfile,[0x00,0x00,0x01,0x04])
		intNameLength = struct.unpack("I", CVRfile[pos:pos + 4])[0]-8
		
		pos+=4
		# And name
		s = str(intNameLength)+"s"
		AnotherName = struct.unpack(s, CVRfile[pos:pos + intNameLength])[0].decode(encoding='UTF-8')
		logging.info(AnotherName)
		self.ModelName2 = AnotherName


		## 00 02 04 0C 00 00 00 nn nn ?? ?? <- nn nn ?? ?? is the number of parts in this object	
		pos = self.findnextcodepos(pos,CVRfile,[0x00,0x02,0x04,0x0C])
		self.int_numberofparts = struct.unpack("I", CVRfile[pos+3:pos + 7])[0]
		logging.info("Number of parts is " + str(self.int_numberofparts))
		
		
		## 00 03 04 0C 00 00 00 nn nn nn nn 	< nn of frames
		pos = self.findnextcodepos(pos,CVRfile,[0x00,0x03,0x04,0x0C])
		self.int_number_of_frames = struct.unpack("I", CVRfile[pos+3:pos + 7])[0]
		logging.info("Number of frames is " + str(self.int_number_of_frames))
	
		
		# lets get the current part's name
		#00 01 04 04	
		pos = self.findnextcodepos(pos,CVRfile,[0x00,0x01,0x04,0x04])
		partnameLength = CVRfile[pos]-8	
		logging.debug("Part name length: " + str(partnameLength))  # for srb the value should be 3
		s = str(partnameLength)+"s"
		pos+=4
		PartName = struct.unpack(s, CVRfile[pos:pos + partnameLength])[0].decode(encoding='UTF-8')
		logging.info(PartName)
		pos+=partnameLength
		
		
		
		# Grab the next parts location!   This could fail in theory (I noticed an animation file didn't have this section)!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		# TODO: , place into a try catch statement as it will fail for some files.
		## I should probably make this throw an error if it isn't correct.	
		pos = self.findnextcodepos(pos,CVRfile,[0x00,0x02,0x04,0x04])
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
		pos+=4
		
		
		
		
	
		
		# Ok.  First thing first.  Is this a multipart mesh or not?  I think it is never the case for multi-part objects, but I could be wrong....
		# The problem is some meshes have it, others don't....
		# The method I use below to figure it out probably isn't right, but hopefully it will work.
		# The idea:  If it is a multimesh, this first one always? has 00 00 00 00 before the 3d data, 
		# I check to see if there is 4 0x00 at that location, if there is, then it is a multimesh.   
		bool_multimesh = CVRfile[pos+28]==0 and CVRfile[pos+29]==0 and CVRfile[pos+30]==0 and CVRfile[pos+31]==0
		logging.info("MultiMesh?: " + str(bool_multimesh))
		
		
		
		
		array_pos = [x0,y0,z0]
		vox_count_section = int_totalvox
		
		
		logging.info(array_pos)
		int_tmpcount1 = 0
		int_tmpcount2 = 0
		
		
		meshnumber = 1
		meshlist =[]
		while int_tmpcount1 < int_totalvox:
			
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
			
			
			tmpMesh = Mesh(meshnumber,array_pos)
			while int_tmpcount2 < vox_count_section:	
				
				#print(int_tmpcount)
				#print(pos)
				if('11010' == self.bytetobinary(CVRfile[pos])[0:5]):
					logging.info("Here it is again")  # didn't find any! on ACP00... but on ones that have multimesh conversions into a single part... its there
					# ok, 
				else:
					
					tmpMesh.addvoxel(pos, self.dict_directions[self.bytetobinary(CVRfile[pos])[0:5]], CVRfile[pos+2], "-1", "-1")
					
				pos+=3
				int_tmpcount2+=1
				int_tmpcount1+=1
				
			meshlist.append(tmpMesh)	
		self.parts.append([PartName, meshlist])	


		
		