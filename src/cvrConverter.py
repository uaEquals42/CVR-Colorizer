#import binascii
import struct
import logging
import time

filename = "C:/Users/Gregory/Desktop/reverse it/ACP00.cvr"

logging.basicConfig(filename='Conversion_log.log', filemode='w', level=logging.INFO)


def bytetobinary(byte):
	#Returns a string of length 8 of the byte of data fed to it.
	#Currently doesn't have any sanity checks on the input data.
	stringxx = bin(byte)[2:]
	while len(stringxx)<8:
		stringxx = "0" + stringxx
	
	
	return stringxx
	
def hextodec(s):
	return int(s, 16)
	
def findnextcodepos(start_pos, filetype, lookupcode):
	#ok, lets do things properly for this
	#the lookupcode should be  4 hex values.  Example [0x00,0x00,0x00,0x02]
	# will return -1 if code is not found further on in file.  
	if(len(lookupcode)!=4):
		raise Exception("Improper lookupcode length")
	
	# filetype is a bytearray
	# start_pos is the position the user wants to start at.
	answer = filetype.index(bytearray((lookupcode[0],lookupcode[1],lookupcode[2],lookupcode[3])),start_pos)+4
	logging.debug("Found " + str(lookupcode)+ " returning position: " + str(answer))
	return answer
	
	
	
	
## This could be completely wrong.  YAY!	
## Below is the lookup chart for knowing what value means which directions.	
"""
	   Y
	   |  /z
	   | /
	   |/
+x---------- (-x)  
	  /|
	 / |
	/  |
"""	

						##   x, y, z    
dict_directions = {'00000':[-1,-1,-1]}	## 00
dict_directions['00001'] = [-1, 0,-1]	## 08
dict_directions['00010'] = [-1,+1,-1]	## 10
dict_directions['00011'] = [ 0,-1,-1]	## 18
dict_directions['00100'] = [ 0, 0,-1]
dict_directions['00101'] = [ 0,+1,-1]	## 28
dict_directions['00110'] = [+1,-1,-1]	## 30
dict_directions['00111'] = [+1, 0,-1]	## 38
dict_directions['01000'] = [+1,+1,-1]	## 40
dict_directions['01001'] = [-1,-1, 0]	## 48
dict_directions['01010'] = [-1, 0, 0]	## 50
dict_directions['01011'] = [-1,+1, 0]	## 58
dict_directions['01100'] = [ 0,-1, 0]	## 60
dict_directions['01101'] = [ 0,+1, 0]	## 68
dict_directions['01110'] = [+1,-1, 0]	## 70
dict_directions['01111'] = [+1, 0, 0]	## 78
dict_directions['10000'] = [+1,+1, 0]	## 80
dict_directions['10001'] = [-1,-1,+1]	## 88
dict_directions['10010'] = [-1, 0,+1]	## 90
dict_directions['10011'] = [-1,+1,+1]	## 98 			
dict_directions['10100'] = [ 0,-1,+1 ]	## A0
dict_directions['10101'] = [ 0, 0,+1 ]	## A8 		
dict_directions['10110'] = [ 0,+1,+1 ]	## B0
dict_directions['10111'] = [+1,-1,+1 ]	## B8
dict_directions['11000'] = [+1, 0,+1]	## C0
dict_directions['11001'] = [+1,+1,+1]	## C8
dict_directions['11010'] = [ 0, 0, 0]	## d0 ??????!!!!!  Noticed this appears only at the end of parts sections for direction for some files!  
## Other files don't have it.	


colors = {}


start_time =  time.time()

with open(filename,"rb") as f:
	filetype = bytearray(f.read())
	logging.info('Opened File')

with open(filename[:-4]+".txt","w") as output:	
	pos = 0
	
	# Read "CVR" from file.  Should always be here.
	cvr = struct.unpack("3s", filetype[0:3])[0].decode(encoding='UTF-8')
	output.write(cvr)
	output.write("\n")
	logging.debug(cvr)
	if(cvr!="CVR"):  # If this isn't there, then this isn't a CVR file.
		raise Exception("Not a CVR file")
	
	
	# How many bytes are there in this file?
	intNumberofbytes = struct.unpack("I", filetype[4:8])[0]
	# Check it to see if they are the same or not
	if(intNumberofbytes==len(filetype)):
		logging.debug("Number of bytes in file" + str(intNumberofbytes))
	else:
		logging.warning("Number of bytes in file (" + str(len(filetype)) + ") does not equals the number of bytes the file thinks it has!"+str(intNumberofbytes))
	
	
	pos = findnextcodepos(pos,filetype,[0x00,0x00,0x00,0x02])
	
	# Ok first we need to get the length of the object name
	dist = struct.unpack("I", filetype[pos:pos + 4])[0]-8
	logging.debug(dist)
	s = str(dist)+"s"  # Then create a filter for unpacking based on it
	
	pos = pos + 4
	
	FileNameitwasconvertedFrom = struct.unpack(s, filetype[pos:pos + dist])[0].decode(encoding='UTF-8')
	output.write(FileNameitwasconvertedFrom)
	output.write("\n")
	logging.info(FileNameitwasconvertedFrom)


	pos = findnextcodepos(pos,filetype,[0x00,0x00,0x00,0x03])
	
	# Where is the 3d data stored in this file?
	threedlocation = struct.unpack("I", filetype[pos:pos+4])[0] + pos - 1
	logging.debug("3d data is at:" + str(threedlocation))
	
	
	# Find the palette name length.
	pos = findnextcodepos(pos,filetype,[0x00,0x00,0x01,0x01])
	dist = filetype[pos]-8 # length of palette name.
	s = str(dist)+"s"
	pos += 4
	
	PaletteName = struct.unpack(s, filetype[pos:pos + dist])[0].decode(encoding='UTF-8')
	output.write(PaletteName)
	output.write("\n")
	logging.info(PaletteName)

	# Palette colors
	pos+=16
	logging.debug("pallet nums" + str(filetype[pos]))
	pos=pos + 1 + 10*3  #10 was the right number for ACP which had 145 for its number. 155-145 = 10
	inttmp = pos + 3*255
	colorcount = 0;
	while pos <= inttmp:
		#print(str(colorcount) +":" + str(filetype[pos]) + "," + str(filetype[pos+1]) +" ," + str(filetype[pos+2]))
		colors[colorcount] = str(filetype[pos]) + "," + str(filetype[pos+1]) +" ," + str(filetype[pos+2])
		colorcount+=1
		pos+=3
	
	
	# Then there is a bunch of stuff I don't know what it does.... O.o
	
	
	# -----------------------------------------------------------------
	
	# Body Parts 3D data
	# Lets work on the fun part!
	pos = threedlocation
	if filetype[threedlocation] == 4:  # Yeah, a 1/256 chance that I'm off by one. 
		# TODO Should make it check a few more bytes...
		logging.debug("Ok, we're likely at the right location.")
	else:
		#terminate
		raise Exception("Not at the right location!")
	
	#No clue about the number in between here means
	#skip for now
	

	# Name length....
	pos = findnextcodepos(pos,filetype,[0x00,0x00,0x01,0x04])
	intNameLength = struct.unpack("I", filetype[pos:pos + 4])[0]-8
	
	pos+=4
	# And name
	s = str(intNameLength)+"s"
	AnotherName = struct.unpack(s, filetype[pos:pos + intNameLength])[0].decode(encoding='UTF-8')
	logging.info(AnotherName)
	output.write(AnotherName)
	output.write("\n")
	#increment the pos
	pos+=intNameLength
	
	
	pos = findnextcodepos(pos,filetype,[0x00,0x02,0x04,0x0C])
	## 00 02 04 0C 00 00 00 nn nn ?? ?? <- nn nn ?? ?? is the number of parts in this object	
	int_numberofparts = struct.unpack("I", filetype[pos+3:pos + 7])[0]
	logging.info("Number of parts is " + str(int_numberofparts))
	
	
	## 00 03 04 0C 00 00 00 nn nn nn nn 	< nn of frames?
	
	pos = findnextcodepos(pos,filetype,[0x00,0x03,0x04,0x0C])
	int_number_of_frames = struct.unpack("I", filetype[pos+3:pos + 7])[0]
	logging.info("Number of frames is " + str(int_number_of_frames))

	
	# lets get the current part's name
	#00 01 04 04	
	pos = findnextcodepos(pos,filetype,[0x00,0x01,0x04,0x04])
	partnameLength = filetype[pos]-8	
	logging.debug("Part name length: " + str(partnameLength))  # for srb the value should be 3
	s = str(partnameLength)+"s"
	pos+=4
	AnotherName = struct.unpack(s, filetype[pos:pos + partnameLength])[0].decode(encoding='UTF-8')
	logging.info(AnotherName)
	output.write(AnotherName)
	output.write("\n")
	pos+=partnameLength
	
	
	
	# Grab the next parts location!   This will fail curently!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	# TODO, place into a try catch statement as it will fail for some files.
	## I should probably make this throw an error if it isn't correct.	
	pos = findnextcodepos(pos,filetype,[0x00,0x02,0x04,0x04])
	nextpart = struct.unpack("I", filetype[pos:pos+4])[0]+pos
	logging.info("Location of next part is " + str(nextpart))
	
	
	
	## There is another distance code here.... not sure why  Not bothering to read it in right now
	
	
	pos = findnextcodepos(pos,filetype,[0x01,0x02,0x04,0x04])
	
	## TODO use id code movement stuff.
	## Does some scalling here.  As far as I can tell.  It will only use one of these.
	int_scale_z = filetype[pos+1+24]
	int_scale_x = filetype[pos+3+24]
	int_scale_y = filetype[pos+5+24]

	# Since the code currently does nothing with these, and the potential of this being important, lets throw a warning if they
	# Don't equal 0
	if(int_scale_z + int_scale_x + int_scale_y != 0):
		logging.warning("Scales z:" + str(int_scale_z) + "  Scales x:" + str(int_scale_x) + "  Scales y:"+ str(int_scale_y))
		logging.warning("Non-zero scaling factor on file!")
	else:
		logging.debug("Scales z:" + str(int_scale_z) + "  Scales x:" + str(int_scale_x) + "  Scales y:"+ str(int_scale_y))
	
	# I'm not sure what these are for.  It affected the view of the object.  Might be length of the stuff.
	# Length?  Perhaps?  Need to see if they match up with anything.
	int_view_z = filetype[pos+24]
	int_view_x = filetype[pos+2+24]
	int_view_y = filetype[pos+4+24]
	logging.info("What? z:" + str(int_view_z) + "  x:" + str(int_view_x) + "  y:"+ str(int_view_y))

	
	## Positional data!  
	z0 = struct.unpack("h", filetype[pos+30:pos+32])[0]
	x0 = struct.unpack("h", filetype[pos+32:pos+34])[0]
	y0 = struct.unpack("h", filetype[pos+34:pos+36])[0]
	logging.debug("Position 0 Z: " + str(z0) + "  x:" + str(x0) + "  y:"+ str(y0))
	
	
	## and then we have the rotation point data of the object	
	zr = struct.unpack("h", filetype[pos+36:pos+38])[0]
	xr = struct.unpack("h", filetype[pos+38:pos+40])[0]
	yr = struct.unpack("h", filetype[pos+40:pos+42])[0]
	logging.info("Rotation Point or Offset? Info Z: " + str(zr) + "  x:" + str(xr) + "  y:"+ str(yr))
	
	
	pos+=42
	# Total Number of voxels
	int_totalvox =  struct.unpack("I", filetype[pos:pos+4])[0]
	logging.info("Total Voxels count " + str(int_totalvox))
	output.write(str(int_totalvox)+"\n")
	
	pos+=4
	
	
	
	
	### This was all in a while loop before.....
	
	"""	
	
	#print(struct.unpack("h", filetype[pos:pos+2])[0])
	z1 = struct.unpack("h", filetype[pos:pos+2])[0]
	x1 = struct.unpack("h", filetype[pos+2:pos+4])[0]
	y1 = struct.unpack("h", filetype[pos+4:pos+6])[0]
	print("x,y,z")
	print("Pos1," + str(x1) + "," + str(y1) + "," + str(z1))
	#output.write("Pos1," + str(x1) + "," + str(y1) + "," + str(z1)+"\n")
	
	#Bunch of stuff inbetween that I think deals with the viewing area.
	#Not really sure.
	#lets... skip it, shall we?
	pos+= 18
	
	z2 = struct.unpack("h", filetype[pos:pos+2])[0]
	x2 = struct.unpack("h", filetype[pos+2:pos+4])[0]
	y2 = struct.unpack("h", filetype[pos+4:pos+6])[0]

	print("Pos2," + str(x2) + "," + str(y2) + "," + str(z2)+"\n")

	
	#output.write("Pos2," + str(x2) + "," + str(y2) + "," + str(z2)+"\n")
	
	
	
	# Now read how many voxels until the next jump
	pos+=6
	vox_count_section = struct.unpack("I", filetype[pos:pos+4])[0]
	print("Voxels " + str(vox_count_section))
	
	pos+=8
	int_tmpcount = 0
	#print(filetype[pos])
	# this currently produces obviously bad location data.
	array_pos = [x1+x2,y1+y2,z1+z2]
	
	"""
	
	# Ok.  First thing first.  Is this a multipart mesh or not?
	#Gonna do kindof a hack here.  Lets first analyze the voxel data for the 
	#11010 marker if there 
	
	
	
	array_pos = [x0,y0,z0]
	int_tmpcount = 0
	vox_count_section = int_totalvox
	
	while int_tmpcount < vox_count_section:	
		#print(int_tmpcount)
		#print(pos)
		if('11010' == bytetobinary(filetype[pos])[0:5]):
			print("Here it is again")  # didn't find any! on ACP00... but on ones that have multimesh conversions into a single part... its there
			# ok, 
		array_pos[0] = array_pos[0] + dict_directions[bytetobinary(filetype[pos])[0:5]][0]
		array_pos[1] = array_pos[1] + dict_directions[bytetobinary(filetype[pos])[0:5]][1]
		array_pos[2] = array_pos[2] + dict_directions[bytetobinary(filetype[pos])[0:5]][2]
		
		#print(dict_directions[bytetobinary(filetype[pos])[0:5]])
		#print(array_pos)
		#print(filetype[pos+2])
		#print(str(colors[filetype[pos+2]]))
		#print(str(int_tmpcount) + ":" + str(vox_count_section))
		output.write(str(array_pos[0]) + "," + str(array_pos[1]) + "," + str( array_pos[2]) +"," + colors[filetype[pos+2]]+"\n")  #bytetobinary(filetype[pos])[-3:] + "," + str(filetype[pos+1]) + "," 
		pos+=3
		int_tmpcount+=1

time_taken = time.time() - start_time		
logging.info("Finished, time taken " + str(time_taken))
print("Finished, time taken " + str(time_taken))
		

	
	
	
