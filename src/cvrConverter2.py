'''
Created on Mar 6, 2014

@author: Gregory
'''
import logging
import CVR

logging.basicConfig(level=logging.DEBUG)			
CVRfile = CVR.CVREngine("C:/Users/Gregory/Desktop/reverse it/allthefiles/Droplet.cvr")

CVRfile.replaceAllcolors(-1, 38)
CVRfile.export("C:/Users/Gregory/Desktop/reverse it/Droplet.txt")
CVRfile.saveColors("C:/Users/Gregory/Desktop/reverse it/Droplet.cvr")	

