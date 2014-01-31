'''
Created on 2014-1-30

@author: bell
'''
import xml.sax
from xml.dom.minidom import parseString

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
        xml.sax.parseString(data, self.__handler)
        return self.__handler.getList()
        
class DOMParser(Parser):
    
    def __init__(self):
        self.__dom=None
        
    def start_parse(self,data,list):
        import types
        self.__dom=parseString(data)
        return self.__find(self.__dom,list)
        
    def __find(self,node,list):
        for each in list:
            _childs=node.getElementsByTagName(each)
            for i in _childs:
                if type(list[each]) == type({}):
                    if type(list[each]) == types.TupleType:
                        list[each].appand(self.__find(i,list[each]))
                    else:
                        list[each]=self.__find(i,list[each])
                else:
                    if type(list[each]) == types.TupleType:
                        list[each].appand(i.nodeValue)
                    else:
                        list[each]=i.nodeValue
        return list
    

if __name__=='__main__':
    parser=DOMParser()
    f=open('D:/milliondata/fairy_select.xml','r')
    list=[{'fairy':[{'serial_id':[]}],'put_down':[]}]
    list=parser.start_parse(f.read(),list)
    f.close()