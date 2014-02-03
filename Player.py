'''
Created on 2014-1-31

@author: bell
'''
#!C:/python27
import Connecter
import Const
import logging
#explorer interface

logger = logging.getLogger('MALogger')

class explorer:
    def __init__(self):
        pass
    def do_explore(self):
        pass
    def __get_info(self):
        pass
    def change_list(self,list,key,value):
        _key=list[key]
        _value=list[value]
        _list={}
        for i in range(0,len(_key)):
            _list[_key[i]]=_value[i]
        return _list
#enemy interface
class enemy:
    def __init__(self):
        pass
    def battle(self):
        pass
    def __get_info(self):
        pass

class User():
    def __init__(self,info):
        __set_info(info)
        
    def __set_info(self,info):
        logger.info('set user info')
        self.ac=info('ac')
        self.bc=info('bc')
        self.gold=info('gold')
        self.gacha_ticket=info('gacha_ticket')
        self.name=info('name')
    
    def update_info(self,info):
        self.__set_info(info)

class Event_Handler():
    def __init__(self):
        pass
    def update_info(self):
        pass

class Player():
    def __init__(self,poster):
        self.__poster=poster
        self.__user_info=None
        self.__area=None
        self.event=Event_Handler()
    def login(self):
        logger.info('get configure')
        self.__get_configure(_content)
        self.__save_session()
            
    def explore(self):
        self.__area=area_explorer(self.__poster)
        self.__area.do_explore()
    
    def __get_info(self):
        _url='menu'
        logger.info('go to main menu')
        _content,_header=self.__poster.post(_url)
        _list={}
        _data=domParser.start_parse(_content,_list)
        f=open('/Users/xtq/million/menu','w')
        f.write(_content)
        f.close()
        return _data
    
    def set_user_info(self):
        if None == self.__user_info:
            self.__user_info=self.__get_info()
        else:
            self.__user_info.update(self.__get_info())
        
        
class floor_explorer(explorer):
    
    def __init__(self,areaID,areaName,poster):
        logger.info('enter area %s' % (areaName))
        self.__area_id=areaID
        self.__area_name=areaName
        self.__poster=poster
        self.__floor_list= self.__get_info()
        self.__now_guild=''
        self.__now_progress=''
        
    def __get_info(self):
        _url='floor'
        _postdata={'area_id':self.__area_id}
        logger.debug('send get_floor post area id=%s' % (self.__area_id))
        _content,_header=self.__poster.post(_url,postdata = _postdata)
        _list={'floor_info':['id','progress','cost']}
        _data=domParser.start_parse(_content,_list)
        #f=open('D:/milliondata/floor1','w')
        #f.write(_content)
        #f.close()
        return  _data['floor_info']
    
    def do_explore(self,update=True):
        if update or '100' == self.__now_progress:
            for each_floor in self.__floor_list:
                if '100' != each_floor['progress'][0]:
                    self.__now_guild=guild_explorer(self.__area_id,self.__area_name,each_floor['id'][0],self.__poster)
                    self.__now_progress=each_floor['progress'][0]
                    break
        _event , self.__now_progress=self.__now_guild.do_explore()
        return _event,self.__now_progress
    
class guild_explorer(explorer):
    
    def __init__(self,areaID,areaName,floorID,poster):
        self.__poster=poster
        self.__floor_ID=floorID
        self.__area_ID=areaID
        self.__area_Name=areaName
        self.__get_info()
        
    def __get_info(self):
        _url='get_floor'
        _postdata={'area_id':self.__area_ID,
                   'check':'1',
                   'floor_id':self.__floor_ID}
        logger.debug('send get_floor post area id=%s' % (self.__area_ID))
        self.__poster.post(_url,postdata = _postdata)
    
    def do_explore(self,auto_build='1',auto_explore='0'):
        _url='guild_explore'
        _postdata={'area_id':self.__area_ID,
                    'floor_id':self.__floor_ID,
                    'auto_build':auto_build,
                    'auto_explore':auto_explore}
        _content,_header=self.__poster.post(_url,postdata = _postdata)
        _list={'your_data':{'ac':'current','bc':'current','free_ap_bc_point':None,},'explore':['progress',]}
        _data=domParser.start_parse(_content,_list)
        return _data,_data['progress'][0]
        
    
class area_explorer(explorer):
    
    def __init__(self,poster):
        logger.info('start to explorer')
        self.__poster=poster
        self.__area_list=self.__get_info()
        self.__now_floor=''
        self.__now_progress=''
        
    def __get_info(self):
        _url='area'
        _content,_header=self.__poster.post(_url)
        _list={'area_info_list':{'area_info':['id','name','prog_area','prog_item','area_type']}}
        return domParser.start_parse(_content,_list)['area_info_list'][0]
    
    def do_explore(self,freeExplore,update=True):
        if update or '100' == self.__now_progress:
            for each_area in self.__area_list['area_info']:
                if '100' != each_area['prog_area'][0]:
                    self.__now_floor=floor_explorer(each_area['id'][0],each_area['name'][0],self.__poster)
                    self.__now_progress=each_floor['progress'][0]
        _event , self.__now_progress = self.__now_floor.do_explore()
        return _event , self.__now_progress
                
class fairy(enemy):
    
    def __init__(self):
        self.__info=self.__get_info()
        
    def __get_info(self):
        _url='fairy_select'
        #_postdata={'area_id':areaID,
        #           'floor_id':floorID,
        #           'auto_build':auto_build,
        #           'auto_explore':auto_explore}
        _content,_header=self.__poster.post(_url)
        _list={'discoverer_id':[],
               'serial_id':[],}
        _data=saxParser.start_parse(_content,_list)
            
        #f=open('D:/milliondata/fairy_select','w')
        #f.write(_content)
        #f.close()
    def battle(self):
        pass
    
        
if __name__ == '__main__':
    player=Player()
    f=open('D:/area','r')
    player.get_area(f.read())