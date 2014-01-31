'''
Created on 2014-1-31

@author: bell
'''
#!C:/python27
import Connecter
import Const
from XMLParser import SAXParser

class Player():
    def __init__(self,poster):
        self.__poster=poster
        self.__xmlParser=SAXParser()
        
    def __change_list(self,list,key,value):
        _key=list[key]
        _value=list[value]
        _list={}
        for i in range(0,len(_key)):
            _list[_key[i]]=_value[i]
        return _list            
        
    def __get_area(self):
        _url='area'
        _content,_header=self.__poster.post(_url)
        
        _list={'id':[],
               'name':[]}
        return self.__change_list(self.__xmlParser.start_parse(_content,_list),'id','name')
    
    def __get_floor(self,areaID):
        _url='floor'
        _postdata={'area_id':areaID}
        _content,_header=self.__poster.post(_url,postdata = _postdata)
        _list={'id':[],
               'progress':[]}
        return self.__change_list(self.__xmlParser.start_parse(_content,_list),'id','progress')
        
    def __do_explore(self,areaID,floorID,auto_explore='0',auto_build='1'):
        _url='guild_explore'
        _postdata={'area_id':areaID,
                   'floor_id':floorID,
                   'auto_build':auto_build,
                   'auto_explore':auto_explore}
        _content,_header=self.__poster.post(_url,postdata = _postdata)
        _list={'id':[],
               'progress':[]}
        _data=self.__xmlParser.start_parse(_content,_list)
        f=open('D:/milliondata/explore%s%s' % (floorID,_data['progress'][0]),'w')
        f.write(_content)
        f.close()
        return _data['progress'][0]
        
    def explore(self):
        _area = self.__get_area()
        _floor = self.__get_floor('108001')
        for each in _floor:
            if '100' != _floor[each]:
                while '100' != self.__do_explore('108001',each):
                    pass
    
    def fairy(self):
        _url='fairy_select'
        #_postdata={'area_id':areaID,
        #           'floor_id':floorID,
        #           'auto_build':auto_build,
        #           'auto_explore':auto_explore}
        _content,_header=self.__poster.post(_url)
        _list={'discoverer_id':[],
               'serial_id':[],}
        _data=self.__xmlParser.start_parse(_content,_list)
        #f=open('D:/milliondata/fairy_select','w')
        #f.write(_content)
        #f.close()
        
    if __name__ == '__main__':
        player=Player()
        f=open('D:/area','r')
        player.get_area(f.read())