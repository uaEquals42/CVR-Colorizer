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




logging.basicConfig(level=logging.INFO)		

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
		self.canvas_top.bind("<B1-Motion>", lambda e: self.paint_pixel(e,self.canvas_top,"top",self.leftcolor))
		self.canvas_top.bind("<Button-1>", lambda e: self.paint_pixel(e,self.canvas_top,"top",self.leftcolor))
		self.canvas_top.bind("<Button-2>", lambda e: self.ChangeZoomLevel(self.canvas_top, "top"))
		self.canvas_top.bind("<B3-Motion>", lambda e: self.paint_pixel(e,self.canvas_top,"top",self.rightcolor))
		self.canvas_top.bind("<Button-3>", lambda e: self.paint_pixel(e,self.canvas_top,"top",self.rightcolor))
		
		lf_left = ttk.Labelframe(frame_views, text='Left')
		self.canvas_left = tk.Canvas(lf_left)
		self.canvas_left.pack()
		lf_left.grid(column=0, row=1)
		self.dict_view_canvas["left"] = self.canvas_left
		self.canvas_left.bind("<B1-Motion>", lambda e: self.paint_pixel(e,self.canvas_left,"left",self.leftcolor))
		self.canvas_left.bind("<Button-1>", lambda e: self.paint_pixel(e,self.canvas_left,"left",self.leftcolor))
		self.canvas_left.bind("<Button-2>", lambda e: self.ChangeZoomLevel(self.canvas_left, "left"))
		self.canvas_left.bind("<B3-Motion>", lambda e: self.paint_pixel(e,self.canvas_left,"left",self.rightcolor))
		self.canvas_left.bind("<Button-3>", lambda e: self.paint_pixel(e,self.canvas_left,"left",self.rightcolor))
		
		lf_front = ttk.Labelframe(frame_views, text='Front')
		self.canvas_front = tk.Canvas(lf_front)
		self.canvas_front.pack()
		lf_front.grid(column=2, row=0)
		self.dict_view_canvas["front"] = self.canvas_left
		self.canvas_front.bind("<B1-Motion>", lambda e: self.paint_pixel(e,self.canvas_front,"front",self.leftcolor))
		self.canvas_front.bind("<Button-1>", lambda e: self.paint_pixel(e,self.canvas_front,"front",self.leftcolor))
		self.canvas_front.bind("<Button-2>", lambda e: self.ChangeZoomLevel(self.canvas_front, "front"))
		self.canvas_front.bind("<B3-Motion>", lambda e: self.paint_pixel(e,self.canvas_front,"front",self.rightcolor))
		self.canvas_front.bind("<Button-3>", lambda e: self.paint_pixel(e,self.canvas_front,"front",self.rightcolor))
		
		lf_bottom = ttk.Labelframe(frame_views, text='Bottom')
		self.canvas_bottom = tk.Canvas(lf_bottom)
		self.canvas_bottom.pack()
		lf_bottom.grid(column=1, row=0)
		self.dict_view_canvas["bottom"] = self.canvas_bottom
		self.canvas_bottom.bind("<B1-Motion>", lambda e: self.paint_pixel(e,self.canvas_bottom,"bottom",self.leftcolor))
		self.canvas_bottom.bind("<Button-1>", lambda e: self.paint_pixel(e,self.canvas_bottom,"bottom",self.leftcolor))
		self.canvas_bottom.bind("<Button-2>", lambda e: self.ChangeZoomLevel(self.canvas_bottom, "bottom"))
		self.canvas_bottom.bind("<B3-Motion>", lambda e: self.paint_pixel(e,self.canvas_bottom,"bottom",self.rightcolor))
		self.canvas_bottom.bind("<Button-3>", lambda e: self.paint_pixel(e,self.canvas_bottom,"bottom",self.rightcolor))
		
		lf_right = ttk.Labelframe(frame_views, text='Right')
		self.canvas_right = tk.Canvas(lf_right)
		self.canvas_right.pack()
		lf_right.grid(column=1, row=1)
		self.dict_view_canvas["right"] = self.canvas_right
		self.canvas_right.bind("<B1-Motion>", lambda e: self.paint_pixel(e,self.canvas_right,"right",self.leftcolor))
		self.canvas_right.bind("<Button-1>", lambda e: self.paint_pixel(e,self.canvas_right,"right",self.leftcolor))
		self.canvas_right.bind("<Button-2>", lambda e: self.ChangeZoomLevel(self.canvas_right, "right"))
		self.canvas_right.bind("<B3-Motion>", lambda e: self.paint_pixel(e,self.canvas_right,"right",self.rightcolor))
		self.canvas_right.bind("<Button-3>", lambda e: self.paint_pixel(e,self.canvas_right,"right",self.rightcolor))
		
		lf_back = ttk.Labelframe(frame_views, text='Back')
		self.canvas_back = tk.Canvas(lf_back)
		self.canvas_back.pack()
		lf_back.grid(column=2, row=1)
		self.dict_view_canvas["back"] = self.canvas_back
		self.canvas_back.bind("<B1-Motion>", lambda e: self.paint_pixel(e,self.canvas_back,"back",self.leftcolor))
		self.canvas_back.bind("<Button-1>", lambda e: self.paint_pixel(e,self.canvas_back,"back",self.leftcolor))
		self.canvas_back.bind("<Button-2>", lambda e: self.ChangeZoomLevel(self.canvas_back, "back"))
		self.canvas_back.bind("<B3-Motion>", lambda e: self.paint_pixel(e,self.canvas_back,"back",self.rightcolor))
		self.canvas_back.bind("<Button-3>", lambda e: self.paint_pixel(e,self.canvas_back,"back",self.rightcolor))
		
	
		frame_meshselect = ttk.Frame(self.root)
		frame_meshselect.grid(column=0, row=1, rowspan=1)
		
		button_left = ttk.Button(frame_meshselect, text='<', command=lambda: print("left"))
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
		while(len(s)<length):
			s = "0"+s
		return s
			
						
	
	def setPaletteColors(self):
		"""
		Goes through the squares on the canvas and assigns them their colors.
		"""
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
		
		self.int_part_number = 0
		self.int_mesh_number = -1
		self.filename = filedialog.askopenfilename(filetypes=(("CVR","*.cvr"),))
		if(len(self.filename)>0):
			logging.info(self.filename)
			try:
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
			except:
				messagebox.showinfo(message='Error: Failed to open file')
				self.quit()
			
		
	def SaveAsFile(self):
		filename = filedialog.asksaveasfilename(filetypes=(("CVR","*.cvr"),))
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
			self.int_mesh_number = self.int_mesh_number + 1
			if self.int_mesh_number >= len(self.CVRfile.return_part(self.int_part_number)[1]):
				self.int_mesh_number = -1
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
	
		#print("Start")
		for mesh2 in part[1]:
			#print(max_dimensions)
			#print(mesh2.dimensions())
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
			#print(max_dimensions)
				
		mesh = part[1][self.int_mesh_number]		
	
		
		xcalc = scale*(abs(max_dimensions[2*xvalue])+abs(max_dimensions[2*xvalue+1]))+20
		ycalc = scale*(abs(max_dimensions[2*yvalue])+abs(max_dimensions[2*yvalue+1]))+20
		canvas_draw.configure(width=xcalc, height=ycalc)
	
		
		if x_direction > 0:
			x_offset = -scale*max_dimensions[2*xvalue]+10  #aka -xmin
		else:
			x_offset = scale*max_dimensions[2*xvalue+1]+10
			
		y_offset = scale*max_dimensions[2*yvalue+1]+10
		
		#print(x_offset)
	
		# ok, for the view it will be x,y and a z.  Z will be kept track of so that we know if something should be in front
		# of something else or not.  
		
		if self.int_mesh_number != -1:
			meshes = [mesh]
		else:
			meshes = part[1]
		
		dict_display = {}  # key is (display_x,display_y)  value is (z, colorhash, (x,y,z))
	
		for mesh in meshes:
			for vox in mesh.voxels:
				test_x = x_direction*vox.location[xvalue]*scale+x_offset
				test_y = -vox.location[yvalue]*scale+y_offset
				
				if(vox.color < len(self.colorhashes)):
					color_hash = self.colorhashes[vox.color]
				else:
					color_hash = self.unknowncolors
				
				if (test_x,test_y) in dict_display:
					if dict_display[(test_x,test_y)][0] < z_direction*vox.location[zvalue]:
						dict_display[(test_x,test_y)] = (z_direction*vox.location[zvalue],color_hash, vox.location)
				else:
					dict_display[(test_x,test_y)] = (z_direction*vox.location[zvalue],color_hash, vox.location)
		
		loc_id_lookup = {}
		id_location_lookup = {}
		# now draw it on the canvas
		for key in dict_display.keys():
			item_id = canvas_draw.create_rectangle(key[0],key[1],key[0]+scale,key[1]+scale, width=0, fill=dict_display[key][1])
			#canvas_draw.tag_bind(id_num,"<Enter>", lambda e, location=dict_display[key][2], intpart=dict_display[key][3], intmesh=dict_display[key][4] : self.paint_pixel(e,location, intpart, intmesh) )
			# this doesn't work as I can't drag the mouse over the time
			loc_id_lookup[dict_display[key][2]] = item_id
			id_location_lookup[item_id] = dict_display[key][2]
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
			
	def paint_pixel(self,event, canvas,view, color):	
		self.previous_location = (event.x, event.y)
		if color >= 0 and color < 256:
			logging.debug(str(event.x) + ","+  str(event.y))
			try:
				pixel_id = canvas.find_overlapping(event.x, event.y, event.x+1, event.y+1)[0]
			except:
				pixel_id = -1
			if pixel_id != -1:
				#print(pixel_id) 
				location = self.id_location_lookup[view][pixel_id]
				logging.debug("Paint Location:" + str(location))
				self.CVRfile.paintVoxel(self.int_part_number,self.int_mesh_number,location,color)
				self.refreshViews(location, color)
	
	def paint_line(self, event, view, color):
		
		delta_x = event.x - self.previous_location[0]
		delta_y = event.y - self.previous_location[1]
		
		if(delta_y==0):
			print("Straight up and down")
		
		self.previous_location = (event.x, event.y)
			
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