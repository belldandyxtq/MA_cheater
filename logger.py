'''
Created on 2014-1-31

@author: bell
'''
#!C:/python27
import logging
import Const

class logger():
    def __init__(self):
        logging.basicConfig(filename=getattr(Const,'LOGFILE'))
    
    def info(self,message):
        logging.info(message)
    
    def warning(self,message):
        logging.info(message)
