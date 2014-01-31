'''
Created on 2014-1-30

@author: bell
'''
import xml.sax


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
    
class XMLParser():
    def __init__(self):
        self.__handler=Handler()
        
    def setList(self,list):
        self.__handler.setList(list)

    def getList(self):
        return self.__handler.getList()
    
    def start_parse(self,data):
        xml.sax.parseString(data, self.__handler)
        
if __name__=='__main__':
    parser=XMLParser()
    f=open('D:/data','r')
    list={'action_id':[]}
    parser.setList(list)
    parser.start_parse(f.read())
    list=parser.getList()
    f.close()
        