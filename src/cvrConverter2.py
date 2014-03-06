'''
Created on Mar 6, 2014

@author: Gregory
'''
import logging
import CVR

logging.basicConfig(level=logging.INFO)			
CVRfile = CVR.CVREngine("C:/Users/Gregory/Desktop/reverse it/A.cvr")

CVRfile.replaceAllcolors(-1, 59)
CVRfile.export("C:/Users/Gregory/Desktop/reverse it/A.txt")
CVRfile.saveColors("C:/Users/Gregory/Desktop/reverse it/test.cvr")	

