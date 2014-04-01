'''
Created on Mar 6, 2014

@author: Gregory Jordan

Copyright (C) 2014  Gregory Jordan

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


https://github.com/uaEquals42/CVR-Colorizer
'''
import logging
import CVR
import math
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import messagebox
import os.path



logging.basicConfig(level=logging.WARNING)		

class app():
	
	def __init__(self):

		self.unknowncolors='#FF00DC'
		self.root = tk.Tk()
		self.root.title("CVR Colorizer 1.0")
		self.root.option_add('*tearOff', tk.FALSE)
		self.colorhashes={}
		self.leftcolor=-1
		self.rightcolor=-1
		self.filename=""
		self.int_part_number = 0
		self.int_mesh_number = -1
		self.location_id_lookup = {}
		self.id_location_lookup = {}
		self.dict_zoom_level = {}
		self.dict_view_canvas = {}
		
		# create a toplevel menu
		menubar = tk.Menu(self.root)
		menu_file = tk.Menu(menubar)
		

		menu_options = tk.Menu(menubar)
		menubar.add_cascade(menu=menu_file, label='File')
		menubar.add_cascade(menu=menu_options, label='Options')
	
		
		menu_file.add_command(label='Open...', command=lambda: self.openFile())
		menu_file.add_command(label='Save As', command=lambda: self.SaveAsFile())
		menu_file.add_command(label='Export', command=lambda: self.ExportFile())
		menu_file.add_command(label='Exit', command=lambda: self.quit())
		
		menu_options.add_command(label='Select color for unknown colors', command=lambda: self.setUknownColors())
		

		
	
		# display the menu
		self.root.config(menu=menubar)
		self.root.columnconfigure(0, weight=1)
		
		
		
		frame_views = ttk.Frame(self.root)
		frame_views.grid(column=0, row=0)
		
	
		
		lf_top = ttk.Labelframe(frame_views, text='Top')
		self.canvas_top = tk.Canvas(lf_top)
		self.canvas_top.pack()
		lf_top.grid(column=0, row=0)
		self.dict_view_canvas["top"] = self.canvas_top
		self.canvas_top.bind("<B1-Motion>", lambda e: self.paint_line(e, "top", self.leftcolor))
		self.canvas_top.bind("<Button-1>", lambda e: self.paint_pixel(e.x, e.y, "top",self.leftcolor))
		self.canvas_top.bind("<Button-2>", lambda e: self.ChangeZoomLevel(self.canvas_top, "top"))
		self.canvas_top.bind("<B3-Motion>", lambda e: self.paint_line(e,"top",self.rightcolor))
		self.canvas_top.bind("<Button-3>", lambda e: self.paint_pixel(e.x, e.y, "top",self.rightcolor))
		
		lf_left = ttk.Labelframe(frame_views, text='Left')
		self.canvas_left = tk.Canvas(lf_left)
		self.canvas_left.pack()
		lf_left.grid(column=0, row=1)
		self.dict_view_canvas["left"] = self.canvas_left
		self.canvas_left.bind("<B1-Motion>", lambda e: self.paint_line(e, "left",self.leftcolor))
		self.canvas_left.bind("<Button-1>", lambda e: self.paint_pixel(e.x, e.y, "left",self.leftcolor))
		self.canvas_left.bind("<Button-2>", lambda e: self.ChangeZoomLevel(self.canvas_left, "left"))
		self.canvas_left.bind("<B3-Motion>", lambda e: self.paint_line(e, "left",self.rightcolor))
		self.canvas_left.bind("<Button-3>", lambda e: self.paint_pixel(e.x, e.y, "left",self.rightcolor))
		
		lf_front = ttk.Labelframe(frame_views, text='Front')
		self.canvas_front = tk.Canvas(lf_front)
		self.canvas_front.pack()
		lf_front.grid(column=2, row=0)
		self.dict_view_canvas["front"] = self.canvas_front
		self.canvas_front.bind("<B1-Motion>", lambda e: self.paint_line(e, "front", self.leftcolor))
		self.canvas_front.bind("<Button-1>", lambda e: self.paint_pixel(e.x, e.y, "front",self.leftcolor))
		self.canvas_front.bind("<Button-2>", lambda e: self.ChangeZoomLevel(self.canvas_front, "front"))
		self.canvas_front.bind("<B3-Motion>", lambda e: self.paint_line(e, "front",self.rightcolor))
		self.canvas_front.bind("<Button-3>", lambda e: self.paint_pixel(e.x, e.y, "front",self.rightcolor))
		
		lf_bottom = ttk.Labelframe(frame_views, text='Bottom')
		self.canvas_bottom = tk.Canvas(lf_bottom)
		self.canvas_bottom.pack()
		lf_bottom.grid(column=1, row=0)
		self.dict_view_canvas["bottom"] = self.canvas_bottom
		self.canvas_bottom.bind("<B1-Motion>", lambda e: self.paint_line(e, "bottom",self.leftcolor))
		self.canvas_bottom.bind("<Button-1>", lambda e: self.paint_pixel(e.x, e.y, "bottom",self.leftcolor))
		self.canvas_bottom.bind("<Button-2>", lambda e: self.ChangeZoomLevel(self.canvas_bottom, "bottom"))
		self.canvas_bottom.bind("<B3-Motion>", lambda e: self.paint_line(e, "bottom",self.rightcolor))
		self.canvas_bottom.bind("<Button-3>", lambda e: self.paint_pixel(e.x, e.y, "bottom",self.rightcolor))
		
		lf_right = ttk.Labelframe(frame_views, text='Right')
		self.canvas_right = tk.Canvas(lf_right)
		self.canvas_right.pack()
		lf_right.grid(column=1, row=1)
		self.dict_view_canvas["right"] = self.canvas_right
		self.canvas_right.bind("<B1-Motion>", lambda e: self.paint_line(e, "right",self.leftcolor))
		self.canvas_right.bind("<Button-1>", lambda e: self.paint_pixel(e.x, e.y, "right",self.leftcolor))
		self.canvas_right.bind("<Button-2>", lambda e: self.ChangeZoomLevel(self.canvas_right, "right"))
		self.canvas_right.bind("<B3-Motion>", lambda e: self.paint_line(e, "right",self.rightcolor))
		self.canvas_right.bind("<Button-3>", lambda e: self.paint_pixel(e.x, e.y, "right",self.rightcolor))
		
		lf_back = ttk.Labelframe(frame_views, text='Back')
		self.canvas_back = tk.Canvas(lf_back)
		self.canvas_back.pack()
		lf_back.grid(column=2, row=1)
		self.dict_view_canvas["back"] = self.canvas_back
		self.canvas_back.bind("<B1-Motion>", lambda e: self.paint_line(e, "back",self.leftcolor))
		self.canvas_back.bind("<Button-1>", lambda e: self.paint_pixel(e.x, e.y, "back",self.leftcolor))
		self.canvas_back.bind("<Button-2>", lambda e: self.ChangeZoomLevel(self.canvas_back, "back"))
		self.canvas_back.bind("<B3-Motion>", lambda e: self.paint_line(e, "back",self.rightcolor))
		self.canvas_back.bind("<Button-3>", lambda e: self.paint_pixel(e.x, e.y, "back",self.rightcolor))
		
	
		frame_meshselect = ttk.Frame(self.root)
		frame_meshselect.grid(column=0, row=1, rowspan=1)
		
		button_left = ttk.Button(frame_meshselect, text='<', command=lambda: self.previous_mesh())
		self.label_current_dispaly = ttk.Label(frame_meshselect, text='?????')
		button_right = ttk.Button(frame_meshselect, text='>', command=lambda: self.next_mesh())
		button_left.grid(column=0, row=0)
		self.label_current_dispaly.grid(column=1, row=0)
		button_right.grid(column=2, row=0)

		self.Colorarea = tk.Canvas(self.root, height=9*20+2, width=640 )
		self.Colorarea.grid(column=0, row=2)
		# I could also use a canvas to generate the color picker....
		r = 2
		column2 = 0
		
		
		while r <= 8*20:
			column2 = 0			
			while column2 < 32:
				bleh = self.Colorarea.create_rectangle((column2*20, r, column2*20+20, r+20), outline='black', fill="white")
				
				self.Colorarea.tag_bind(bleh, "<Button-1>", lambda e: self.setleftcolor(e))
				self.Colorarea.tag_bind(bleh, "<Button-3>", lambda e: self.setrightcolor(e))
				
				column2 = column2 + 1
				
			r = r + 20
		
		self.Colorchoise = tk.Canvas(self.root, height=50, width=50 )
		self.Colorchoise.create_rectangle((17,17,47,47), fill="white")
		self.Colorchoise.create_rectangle((2,2,32,32), fill="white")
		
		self.Colorchoise.grid(column=0, row=3)
		
		
		self.root.mainloop()	
	
	def setUknownColors(self):
		self.unknowncolors = colorchooser.askcolor(initialcolor=self.unknowncolors)[1]
		if len(self.filename)!=0:
			self.setPaletteColors()
			self.create_views()
		
	def ChangeZoomLevel(self, canvas, view):
		if self.dict_zoom_level[view] == 1:
			self.dict_zoom_level[view] = 2
		else:
			self.dict_zoom_level[view] = 1
		self.drawMesh(view, canvas)
	
	def makestringlonger(self, s, length):
		'''
		Used for making the hex values the same length.
		:param s:  string
		:param length: 
		'''
		
		while(len(s)<length):
			s = "0"+s
		return s
			
						
	
	def setPaletteColors(self):
		'''
		Goes through the squares on the canvas and assigns them their colors.
		'''
		if len(self.filename)!=0:
			i = 0
			while i < len(self.CVRfile.dict_colors):
				r = hex(int(self.CVRfile.dict_colors[i].split(",")[0]))[2:]
				g = hex(int(self.CVRfile.dict_colors[i].split(",")[1]))[2:]
				b = hex(int(self.CVRfile.dict_colors[i].split(",")[2]))[2:]
				r = self.makestringlonger(r, 2)
				g = self.makestringlonger(g, 2)
				b = self.makestringlonger(b, 2)
				
				
				fillcolor = "#"+r+g+b
				self.colorhashes[i] = fillcolor
				self.Colorarea.itemconfig(i+1, fill=fillcolor) 
				i = i + 1
			while i <= 256:
				self.Colorarea.itemconfig(i+1, fill=self.unknowncolors) 
				
				i = i + 1
		
	
	def openFile(self):
		
		# First see if we have an option file.
		savelocation = "No save location"
		if os.path.isfile("options.txt"):
			with open("options.txt","r") as f:
				openlocation = f.readline().strip()
				savelocation = f.readline().strip()
			
				if os.path.exists(os.path.abspath(openlocation)) != True:
					openlocation = os.path.expanduser("~")
					
		else:
			openlocation = os.path.expanduser("~")
		
		self.int_part_number = 0
		self.int_mesh_number = -1
		# Get the filename!
		logging.info(openlocation)
		self.filename = filedialog.askopenfilename(filetypes=(("CVR","*.cvr"),),initialdir=openlocation)
		
		# Set this as the new filename if valid in the options file.
		if os.path.isfile(self.filename):
			with open("options.txt","w") as f:
				directory = os.path.dirname(os.path.abspath(self.filename))
				f.write(directory + " \n")
				f.write(savelocation)
		
			logging.info(self.filename)
			#try:
			self.CVRfile = CVR.CVREngine(self.filename)
			self.setPaletteColors()
			self.dict_zoom_level["left"] = 1
			self.dict_zoom_level["right"] = 1
			self.dict_zoom_level["top"] = 1
			self.dict_zoom_level["bottom"] = 1
			self.dict_zoom_level["front"] = 1
			self.dict_zoom_level["back"] = 1
			self.create_views()
			
			self.leftcolor=-1
			self.rightcolor=-1
			self.Colorchoise.itemconfig(1, fill="white")
			self.Colorchoise.itemconfig(2, fill="white")
			#except:
				#messagebox.showinfo(message='Error: Failed to open file')
				#self.quit()
			self.set_descriptor_text()
		else:
			self.filename=""
			
	def SaveAsFile(self):
		
		# First see if we have an option file.
		savelocation = "No save location"
		if os.path.isfile("options.txt"):
			with open("options.txt","r") as f:
				openlocation = f.readline().strip()
				savelocation = f.readline().strip()
				
				if os.path.exists(os.path.abspath(savelocation)) != True:
					savelocation = openlocation
					if os.path.exists(os.path.abspath(savelocation)) != True:
						savelocation = savelocation = os.path.expanduser("~")
					
		else:
			savelocation = os.path.expanduser("~")
			# This should never happen.
			# will only happen if a user deletes the option file while the program is running.
		
		filename = filedialog.asksaveasfilename(filetypes=(("CVR","*.cvr"),),initialdir=savelocation)
		
		# Set this as the new filename if valid in the options file.
		if len(filename)>0:
			with open("options.txt","w") as f:
				directory = os.path.dirname(os.path.abspath(filename))
				f.write(openlocation + " \n")
				f.write(directory)
		
		
			logging.info(filename)
			self.CVRfile.saveColors(filename)
		
		
	def ExportFile(self):
		filename = filedialog.asksaveasfilename(filetypes=(("Text","*.txt"),),title="Export")
		filename=filename+".txt"
		logging.info(filename)
		self.CVRfile.export(filename)
		
	def quit(self):
		self.root.quit()
	
	def next_mesh(self):
		
		if len(self.filename) > 0:
			number_of_meshes = len(self.CVRfile.return_part(self.int_part_number)[1])
			if number_of_meshes > 1:
				self.int_mesh_number = self.int_mesh_number + 1
				if self.int_mesh_number >= number_of_meshes:
					self.int_mesh_number = -1
				self.set_descriptor_text()
				self.create_views()
	def previous_mesh(self):
		
		if len(self.filename) > 0:
			number_of_meshes = len(self.CVRfile.return_part(self.int_part_number)[1])
			if number_of_meshes > 1:
				self.int_mesh_number = self.int_mesh_number - 1
				if self.int_mesh_number < -1:
					self.int_mesh_number = number_of_meshes-1
				self.set_descriptor_text()
				self.create_views()	
		
	def set_descriptor_text(self):
		pname = self.CVRfile.part_name(self.int_part_number)
		if self.int_mesh_number == -1:
			mname = "Mesh: All"
		else:
			mname = self.CVRfile.returnMesh(self.int_part_number, self.int_mesh_number).meshname
		self.label_current_dispaly.configure(text=pname+": " + mname)
		
	def create_views(self):
		
		
		self.drawMesh('left', self.canvas_left)
		self.drawMesh('right', self.canvas_right)
		self.drawMesh('top', self.canvas_top)
		self.drawMesh('bottom',  self.canvas_bottom)
		self.drawMesh('front',  self.canvas_front)
		self.drawMesh('back',  self.canvas_back)
		
	
	def calc_colorhash(self, color):
		if(color < len(self.colorhashes)):
			color_hash = self.colorhashes[color]
		else:
			color_hash = self.unknowncolors
		return color_hash
		
	def drawMesh(self, view, canvas_draw):

		scale = self.dict_zoom_level[view]
		logging.debug("Draw the mesh to canvas")
		yvalue = 1
		
		if view=="top":
			xvalue = 2 
			zvalue = 1 
			yvalue = 0
			z_direction = +1
			x_direction = +1
		if view=="bottom":
			xvalue = 2 
			zvalue = 1 
			yvalue = 0
			z_direction = -1
			x_direction = -1
		if view=="right":
			xvalue = 0 # x = x
			zvalue = 2 # z = z
			z_direction = +1
			x_direction = +1
		if view=="left":
			xvalue = 0 
			zvalue = 2 
			z_direction = -1
			x_direction = -1
		if view=="back":
			xvalue = 2 
			zvalue = 0 
			z_direction = -1
			x_direction = +1
		if view=="front":
			xvalue = 2 # use z for the screenspace x value
			zvalue = 0 #z = x
			z_direction = +1
			x_direction = -1  # We want the screenspace x value to go the opposite direction
		canvas_draw.delete(tk.ALL)

		#ok for test purposes lets render from one side first
		#self.canvas_left.
		logging.debug(self.CVRfile.filename)
		
		part = self.CVRfile.parts[self.int_part_number]
		#ok lets first see if the viewing area is big enough for the object...
		#lets make it big enough for all the meshes for the current part.
		max_dimensions = []
		for tmp_var in part[1][0].dimensions():
			max_dimensions.append(tmp_var)
	

		for mesh2 in part[1]:

			if max_dimensions[0] > mesh2.dimensions()[0]:
				max_dimensions[0] = mesh2.dimensions()[0]
			if max_dimensions[1] < mesh2.dimensions()[1]:
				max_dimensions[1] = mesh2.dimensions()[1]
			if max_dimensions[2] > mesh2.dimensions()[2]:
				max_dimensions[2] = mesh2.dimensions()[2]
			if max_dimensions[3] < mesh2.dimensions()[3]:
				max_dimensions[3] = mesh2.dimensions()[3]
			if max_dimensions[4] > mesh2.dimensions()[4]:
				max_dimensions[4] = mesh2.dimensions()[4]
			if max_dimensions[5] < mesh2.dimensions()[5]:
				max_dimensions[5] = mesh2.dimensions()[5]

				
		mesh = part[1][self.int_mesh_number]		
	
		
		xcalc = scale*(abs(max_dimensions[2*xvalue])+abs(max_dimensions[2*xvalue+1]))+20
		ycalc = scale*(abs(max_dimensions[2*yvalue])+abs(max_dimensions[2*yvalue+1]))+20
		canvas_draw.configure(width=xcalc, height=ycalc)
	
		
		if x_direction > 0:
			x_offset = -scale*max_dimensions[2*xvalue]+10  #aka -xmin
		else:
			x_offset = scale*max_dimensions[2*xvalue+1]+10
			
		y_offset = scale*max_dimensions[2*yvalue+1]+10
		

	
		# ok, for the view it will be x,y and a z.  Z will be kept track of so that we know if something should be in front
		# of something else or not.  
		
		if self.int_mesh_number != -1:
			meshes = [mesh]
		else:
			meshes = part[1]
		
		dict_display = {}  # loc_xy is (display_x,display_y)  value is (z, colorhash, (x,y,z))
	
		for mesh in meshes:
			for location, vox_list in mesh.dict_voxels.items():
				vox = vox_list[0]
				#for vox in mesh.voxels:
				test_x = x_direction*location[xvalue]*scale+x_offset
				test_y = -location[yvalue]*scale+y_offset
				
				
				
				tmp_xy = (test_x,test_y)
				tmp_pixel_value = dict_display.get(tmp_xy) # can't use for setting the value again.
				if tmp_pixel_value!=None:
					if tmp_pixel_value[0] < z_direction*location[zvalue]:
						color_hash = self.calc_colorhash(vox.color)
						dict_display[tmp_xy] = (z_direction*location[zvalue],color_hash, location)
				else:
					color_hash = self.calc_colorhash(vox.color)
					dict_display[tmp_xy] = (z_direction*location[zvalue],color_hash, location)
		
		loc_id_lookup = {}
		id_location_lookup = {}
		# now draw it on the canvas
		for loc_xy, value in dict_display.items():
			locationxyz = value[2]
			
			item_id = canvas_draw.create_rectangle(loc_xy[0],loc_xy[1],loc_xy[0]+scale,loc_xy[1]+scale, width=0, fill=value[1])
			loc_id_lookup[locationxyz] = item_id
			id_location_lookup[item_id] = locationxyz
			
		self.location_id_lookup[view] = loc_id_lookup
		self.id_location_lookup[view] = id_location_lookup
	
	def updateView(self, view, location, canvas, color):
		if location in self.location_id_lookup[view]:
			if color in self.colorhashes:
				canvas.itemconfigure(self.location_id_lookup[view][location], fill=self.colorhashes[color])
			else:
				canvas.itemconfigure(self.location_id_lookup[view][location], fill=self.unknowncolors)

		
	
	def refreshViews(self, location, color):
		self.updateView("top", location, self.canvas_top, color)
		self.updateView("bottom", location, self.canvas_bottom, color)
		self.updateView("right", location, self.canvas_right, color)
		self.updateView("left", location, self.canvas_left, color)
		self.updateView("back", location, self.canvas_back, color)
		self.updateView("front", location, self.canvas_front, color)
			
	def paint_pixel(self, x,y, view, color):	
		self.previous_location = (x, y)
		if color >= 0 and color < 256:
			logging.debug(str(x) + ","+  str(y))
			try:
				pixel_id = self.dict_view_canvas[view].find_overlapping(x, y, x+1, y+1)[0]
			except:
				pixel_id = -1
			if pixel_id != -1:

				location = self.id_location_lookup[view][pixel_id]
				logging.debug("Paint Location:" + str(location))
				self.CVRfile.paintVoxel(self.int_part_number,self.int_mesh_number,location,color)
				self.refreshViews(location, color)
	
	def paint_line(self, event, view, color):
		"""
		Bresenham's line algorithm
		
		"""
		
		x1 = event.x
		y1 = event.y
		x0 = self.previous_location[0]
		y0 = self.previous_location[1]
		
		
		
		delta_x = abs(x1-x0)
		delta_y = abs(y1-y0) 
		if x0 < x1:
			sx = 1 
		else: 
			sx = -1
		if y0 < y1:
			sy = 1
		else:
			sy = -1
			
		err = delta_x-delta_y
		
		
		while True:
	
			self.paint_pixel(x0,y0,view,color)
			
			if x0==x1 and y0==y1:
				break
			
			e2 = 2 * err
			if e2 > -delta_y:
				err = err - delta_y
				x0 = x0 + sx
			if e2 < delta_x:
				err = err + delta_x
				y0 = y0 + sy 

		self.paint_pixel(x0,y0,view,color)
		self.previous_location = (x0, y0)
			
	def setleftcolor(self,e):	
		if(len(self.filename)>0):
			
			self.leftcolor = (math.floor((e.y-2)/20)) * 32 + math.floor(e.x/20)
			logging.info(self.leftcolor)
			if(self.leftcolor < len(self.colorhashes)):
				self.Colorchoise.itemconfigure(2, fill=self.colorhashes[self.leftcolor])
			else:
				self.Colorchoise.itemconfigure(2, fill=self.unknowncolors)
		
		
	def setrightcolor(self,e):	
		if(len(self.filename)>0):
			
			self.rightcolor = (math.floor((e.y-2)/20)) * 32 + math.floor(e.x/20)
			logging.info(self.rightcolor)
			if(self.rightcolor < len(self.colorhashes)):
				self.Colorchoise.itemconfigure(1, fill=self.colorhashes[self.rightcolor])
			else:
				self.Colorchoise.itemconfigure(1, fill=self.unknowncolors)
						


	
app()