'''
Created on 2014-1-30

@author: bell
'''
import xml.sax
import logging
from xml.dom.minidom import parseString
logger = logging.getLogger('MALogger')
#private
#used to collect data

class Parser:
    def __init__(self):
        pass
    def start_parse(self,data,list):
        pass
    
    
class Handler(xml.sax.handler.ContentHandler):

    def __init__(self):
        self.__flag=False
        self.__tag=''
        self.__list={}
        
    def setList(self,list):
        self.__list=list
        
    def startElement(self,name,attr):
        if name in self.__list:
            self.__flag=True
            self.__tag=name
            
    def characters(self,content):
        if  self.__flag:
            list=self.__list[self.__tag]
            list.append(content)
            self.__flag=False
            
    def getList(self):
        return self.__list

#public
#used to parse XML and get data
#usage:
#create object ,start_parse: XMLDATA, a dictionary store attribute to get(string : tupple)
class SAXParser(Parser):
    def __init__(self):
        self.__handler=Handler()
        
    def start_parse(self,data,list):
        self.__handler.setList(list)
        try:
            xml.sax.parseString(data, self.__handler)
        except:
            raise RuntimeError
        try:
            return self.__handler.getList()
        except:
            raise ValueError
        
class DOMParser(Parser):
    
    def __init__(self):
        self.__dom=None
        
    def start_parse(self,data,list):
        try:
            self.__dom=parseString(data)
        except:
            raise RuntimeError
        import types
        return self.__find(self.__dom,list)
        
    def __find(self,node,list):
        _ans={}
        for _attr in list:
            _now=node.getElementsByTagName(_attr)
            _ans[_attr]=[]
            if type({}) != type(list):
                for _child in _now:
                    _ans[_attr].append(_child.childNodes[0].nodeValue)
            else:
                for _child in _now:
                    _ans[_attr].append(self.__find(_child, list[_attr]))
        return _ans
    
if __name__=='__main__':
    parser=DOMParser()
    f=open('D:/milliondata/areabell','r')
    list={'area_info_list':{'area_info':['id','name','prog_area','prog_item','area_type']}}
    list=parser.start_parse(f.read(),list)
    f.close()