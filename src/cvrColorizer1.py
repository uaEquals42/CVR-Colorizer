'''
Created on Mar 6, 2014

@author: Gregory Jordan
'''
import logging
import CVR
import math
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import colorchooser


logging.basicConfig(level=logging.INFO)		

class app():
	
	leftcolor=-1
	rightcolor=-1
	filename=""
	
	
	def makestringlonger(self, s, length):
		while(len(s)<length):
			s = "0"+s
		return s
			
						
	
	def setPaletteColors(self):
		i = 0
		while i < len(self.CVRfile.dict_colors):
			#print(self.CVRfile.dict_colors[i].replace(",",""))
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
		self.filename = filedialog.askopenfilename(filetypes=(("CVR","*.cvr"),))
		if(len(self.filename)>0):
			logging.info(self.filename)
			
			self.CVRfile = CVR.CVREngine(self.filename)
			self.setPaletteColors()
			self.updateviews()
		
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
	
	def updateviews(self):
		print
		mesh = self.CVRfile.returnMesh()
		self.drawMesh('left', mesh, self.canvas_left)
		self.drawMesh('right', mesh, self.canvas_right)
		self.drawMesh('top', mesh, self.canvas_top)
		self.drawMesh('bottom', mesh, self.canvas_bottom)
		self.drawMesh('front', mesh, self.canvas_front)
		self.drawMesh('back', mesh, self.canvas_back)
		
		
	def drawMesh(self, view, mesh, canvas_draw):
		logging.info("Draw the mesh to canvas")
		canvas_draw.delete(ALL)
		#ok for test purposes lets render from one side first
		#self.canvas_left.
		print(self.CVRfile.filename)
		
		print(mesh.dimensions())
		#ok lets first see if the viewing area is big enough for the object...
		xcalc = 2*(abs(mesh.dimensions()[0])+abs(mesh.dimensions()[1]))+40
		ycalc = 2*(abs(mesh.dimensions()[2])+abs(mesh.dimensions()[3]))+40
		canvas_draw.configure(width=xcalc, height=ycalc)
	
		
			
		x_offset = -2*mesh.dimensions()[0]+10  #aka -xmin
		y_offset = 2*mesh.dimensions()[3]+10
		
		
	
		# ok, for the view it will be x,y and a z.  Z will be kept track of so that we know if something should be in front
		# of something else or not.  
		
		
		
		dict_display = {}  # key is (display_x,display_y)  value is (z, colorhash, (x,y,z))
		for vox in mesh.voxels:
			test_x = vox.location[0]*2+x_offset
			test_y = -vox.location[1]*2+y_offset
			if (test_x,test_y) in dict_display:
				if dict_display[(test_x,test_y)][0] < vox.location[2]:
					dict_display[(test_x,test_y)] = (vox.location[2],self.colorhashes[vox.color], vox.location)
			else:
				dict_display[(test_x,test_y)] = (vox.location[2],self.colorhashes[vox.color], vox.location)
		
		# now draw it on the canvas
		for key in dict_display.keys():
			canvas_draw.create_rectangle(key[0],key[1],key[0]+2,key[1]+2, width=0, fill=dict_display[key][1])
		
		
	def setleftcolor(self,e):	
		if(len(self.filename)>0):
			
			self.leftcolor = (math.floor((e.y-2)/20)) * 32 + math.floor(e.x/20)
			logging.info(self.leftcolor)
			if(self.leftcolor < len(self.colorhashes)):
				self.Colorchoise.itemconfigure(2, fill=self.colorhashes[self.leftcolor])
			else:
				self.Colorchoise.itemconfigure(2, fill=self.unknowncolors)
			
	def __init__(self):
		self.unknowncolors='#FF00DC'
		self.root = Tk()
		self.root.title("CVR Colorizer 1.0")
		self.root.option_add('*tearOff', FALSE)
		self.colorhashes={}
		# create a toplevel menu
		menubar = Menu(self.root)
		menu_file = Menu(menubar)
		
		menu_view = Menu(menubar)
		menu_options = Menu(menubar)
		menubar.add_cascade(menu=menu_file, label='File')
		menubar.add_cascade(menu=menu_options, label='Options')
		menubar.add_cascade(menu=menu_view, label='Views')
		
		menu_file.add_command(label='Open...', command=lambda: self.openFile())
		menu_file.add_command(label='Save As', command=lambda: self.SaveAsFile())
		menu_file.add_command(label='Export', command=lambda: self.ExportFile())
		menu_file.add_command(label='Exit', command=lambda: self.quit())
		
		menu_options.add_command(label='Select color for unknown colors', command=lambda: colorchooser.askcolor(initialcolor=self.unknowncolors))
		
		str_front = StringVar()
		str_left = StringVar()
		str_back = StringVar()
		str_right = StringVar()
		str_top = StringVar()
		str_bottom = StringVar()
		str_left.initialize(1)
		menu_view.add_checkbutton(label='Front', variable=str_front, onvalue=1, offvalue=0)
		menu_view.add_checkbutton(label='Left', variable=str_left, onvalue=1, offvalue=0)
		menu_view.add_checkbutton(label='Back', variable=str_back, onvalue=1, offvalue=0)
		menu_view.add_checkbutton(label='Right', variable=str_right, onvalue=1, offvalue=0)
		menu_view.add_checkbutton(label='Top', variable=str_top, onvalue=1, offvalue=0)
		menu_view.add_checkbutton(label='Bottom', variable=str_bottom, onvalue=1, offvalue=0)
		
	
		# display the menu
		self.root.config(menu=menubar)
		self.root.columnconfigure(0, weight=1)
		
		frame_views = ttk.Frame(self.root)
		frame_views.grid(column=0, row=0)
		
		lf_top = ttk.Labelframe(frame_views, text='Top')
		self.canvas_top = Canvas(lf_top)
		self.canvas_top.pack()
		lf_top.grid(column=0, row=0)
		
		lf_left = ttk.Labelframe(frame_views, text='Left')
		self.canvas_left = Canvas(lf_left)
		self.canvas_left.pack()
		lf_left.grid(column=1, row=0)
		
		lf_front = ttk.Labelframe(frame_views, text='Front')
		self.canvas_front = Canvas(lf_front)
		self.canvas_front.pack()
		lf_front.grid(column=2, row=0)
		
		lf_bottom = ttk.Labelframe(frame_views, text='Bottom')
		self.canvas_bottom = Canvas(lf_bottom)
		self.canvas_bottom.pack()
		lf_bottom.grid(column=0, row=1)
		
		lf_right = ttk.Labelframe(frame_views, text='Right')
		self.canvas_right = Canvas(lf_right)
		self.canvas_right.pack()
		lf_right.grid(column=1, row=1)
		
		lf_back = ttk.Labelframe(frame_views, text='Back')
		self.canvas_back = Canvas(lf_back)
		self.canvas_back.pack()
		lf_back.grid(column=2, row=1)
		
	
		frame_meshselect = ttk.Frame(self.root)
		frame_meshselect.grid(column=0, row=1)
		
		button_left = ttk.Button(frame_meshselect, text='<-', command=lambda: print("left"))
		label_current_dispaly = ttk.Label(frame_meshselect, text='Middle:')
		button_right = ttk.Button(frame_meshselect, text='->', command=lambda: print("Right"))
		button_left.grid(column=0, row=0)
		label_current_dispaly.grid(column=1, row=0)
		button_right.grid(column=2, row=0)

		self.Colorarea = Canvas(self.root, height=9*20+2, width=640 )
		self.Colorarea.grid(column=0, row=2)
		# I could also use a canvas to generate the color picker....
		r = 2
		column2 = 0
		
		
		while r <= 8*20:
			column2 = 0			
			while column2 < 32:
				bleh = self.Colorarea.create_rectangle((column2*20, r, column2*20+20, r+20), outline='black', fill="white")
				
				self.Colorarea.tag_bind(bleh, "<Button-1>", lambda e: self.setleftcolor(e))
				
				column2 = column2 + 1
				
			r = r + 20
		
		self.Colorchoise = Canvas(self.root, height=50, width=50 )
		self.Colorchoise.create_rectangle((17,17,47,47), fill="white")
		self.Colorchoise.create_rectangle((2,2,32,32), fill="white")
		
		self.Colorchoise.grid(column=0, row=3)
		
		
		self.root.mainloop()

	
app()