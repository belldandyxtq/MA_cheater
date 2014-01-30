'''
Created on 2014-1-30

@author: bell
'''
from xml.dom.minidom import parse, parseString

class XMLParser():
    def __init__(self,xml):
        self.__dom=parseString(xml)
        
    def get_data(self,list):
        dict={}
        for element in list:
            dict[element]=self.__dom.getElementById(element)
            
        return dict
        