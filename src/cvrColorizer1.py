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

logging.basicConfig(level=logging.DEBUG)		

class app():
	
	leftcolor=-1
	rightcolor=-1
	filename=""
	colorhashes={}
	
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
			self.Colorarea.itemconfig(i+1, fill="white") 
			
			i = i + 1
		
	
	def openFile(self):
		self.filename = filedialog.askopenfilename(filetypes=(("CVR","*.cvr"),))
		if(len(self.filename)>0):
			logging.info(self.filename)
			self.CVRfile = CVR.CVREngine(self.filename)
			self.setPaletteColors()
		
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
		
	def drawMesh(self):
		logging.info("Draw the mesh to canvas")
	
	def setleftcolor(self,e):	
		if(len(self.filename)>1):
			self.leftcolor = (math.floor((e.y-2)/20)) * 32 + math.floor(e.x/20)
			logging.info(self.leftcolor)
			self.Colorchoise.itemconfigure(2, fill=self.colorhashes[self.leftcolor])
			
	def __init__(self):
		self.root = Tk()
		self.root.title("CVR Colorizer 1.0")
		self.root.option_add('*tearOff', FALSE)
		
		# create a toplevel menu
		menubar = Menu(self.root)
		menu_file = Menu(menubar)
		
		menu_view = Menu(menubar)
		menubar.add_cascade(menu=menu_file, label='File')
		
		menubar.add_cascade(menu=menu_view, label='Views')
		
		menu_file.add_command(label='Open...', command=lambda: self.openFile())
		menu_file.add_command(label='Save As', command=lambda: self.SaveAsFile())
		menu_file.add_command(label='Export', command=lambda: self.ExportFile())
		menu_file.add_command(label='Exit', command=lambda: self.quit())
		
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
		
		left = ttk.Labelframe(self.root, text='Left')
		canvas = Canvas(left)
		canvas.pack()
		left.grid(column=0, row=0)
	

		self.Colorarea = Canvas(self.root, height=9*20+2, width=640 )
		self.Colorarea.grid(column=0, row=1)
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
		
		self.Colorchoise.grid(column=0, row=2)
		
		
		self.root.mainloop()

	
app()