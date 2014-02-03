'''
Created on 2014-1-31

@author: bell
'''
#!C:/python27
from Connecter import Poster
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
        self.__set_info(info)
        self.gacha_ticket=info['gacha_ticket']
        self.name=info['name']
        
    def __set_info(self,info):
        logger.info('set user info')
        self.ap=info['ap']
        self.bc=info['bc']
        self.gold=info['gold']

    
    def update_info(self,info):
        self.__set_info(info)

class Event_Handler():
    def __init__(self):
        pass
    def update_info(self):
        pass

class Player():
    def __init__(self,location,username,passwd):
        self.__poster=Poster(location,username,passwd)
        self.__user_info=None
        self.__area=None
        self.event=Event_Handler()
        
    def login(self):
        _data=self.__poster.login()
        logger.info('get configure')
        self.set_user_info()
        #self.__get_configure(_data)
            
    def explore(self):
        self.__area=area_explorer(self.__poster)
        self.__area.do_explore()
    
    def __get_info(self):
        _url='menu'
        logger.info('go to main menu')
        _list={'your_data':{'name':[],'townlevel':'','gold':'','cp':'','ap':['current','max'],'bc':['current','max'],
                           'free_ap_bc_point':[],'gacha_ticket':[]}}
        _content,_header=self.__poster.post(_url,list=_list,use_2nd_key=False)
        return _content['your_data'][0]
    
    def set_user_info(self):
        if None == self.__user_info:
            self.__user_info=User(self.__get_info())
        else:
            self.__user_info.update(self.__get_info())
            
    def private_fairy(self):
        self.__fairy=fairy(self.__poster)
        self.__fairy.battle()
        
    def guild_fairy(self):
        self.__guild_fairy=guid_fairy(self.__poster)
        
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
        _list={'floor_info':['id','progress','cost']}
        logger.debug('send get_floor post area id=%s' % (self.__area_id))
        _data , _head=self.__poster.post(_url,'dom',_list,postdata = _postdata)
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
        _list={'your_data':{'ap':['current'],'bc':['current'],'free_ap_bc_point':''},'explore':['progress']}
        _data , _head=self.__poster.post(_url,'dom',_list,postdata = _postdata)
        _progress=_data['explore'][0]
        return _data,_progress['progress'][0]
        
    
class area_explorer(explorer):
    
    def __init__(self,poster):
        logger.info('start to explorer')
        self.__poster=poster
        self.__area_list=self.__get_info()
        self.__now_floor=''
        self.__now_progress=''
        
    def __get_info(self):
        _url='area'
        _list={'area_info_list':{'area_info':['id','name','prog_area','prog_item','area_type']}}
        _content,_head=self.__poster.post(_url,'dom',_list)

        return _content['area_info_list'][0]
    
    def do_explore(self,freeExplore=False,update=True):
        if update or '100' == self.__now_progress:
            for each_area in self.__area_list['area_info']:
                if '100' != each_area['prog_area'][0]:
                    self.__now_floor=floor_explorer(each_area['id'][0],each_area['name'][0],self.__poster)
                    self.__now_progress=each_area['prog_area'][0]
                    break
        _event , self.__now_progress = self.__now_floor.do_explore()
        return _event , self.__now_progress
                
class fairy(enemy):
    
    def __init__(self,poster):
        self.__poster=poster
        self.__fairy_list,self.__rewards = self.__get_info()

    def __get_info(self):
        _url='fairy_select'
        _list={'fairy_select': {'user': ['id', 'name'],'fairy_event': {'fairy': ['serial_id','name', 'lv', 'hp', 'hp_max', 'discoverer_id', 'rare_flg'],'put_down': '','reward_status': ''}}}
        _content,_header=self.__poster.post(_url,postdata={},list=_list)
        return self.__change_list(_content['fairy_select'][0])
        
    def __change_list(self,data):
        _rewards=[]
        _user={}
        for each_user in data['user']:
            _user[each_user['id'][0]]=each_user['name'][0]
        _fairy=[]
        for each_fairy in data['fairy_event']:
            _now_fairy=each_fairy['fairy'][0]
            _fairy_data={}
            _fairy_data['serial_id']=_now_fairy['serial_id'][0]
            _fairy_data['name']=_now_fairy['name'][0]
            _fairy_data['lv']=_now_fairy['lv'][0]
            _fairy_data['hp']=_now_fairy['hp'][0]
            _fairy_data['hp_max']=_now_fairy['hp_max'][0]
            _fairy_data['rare_flg']=_now_fairy['rare_flg'][0]
            _fairy_data['discoverer_id']=_now_fairy['discoverer_id'][0]
            _fairy_data['discoverer_name'] = _user[_fairy_data['discoverer_id']]
            _fairy_data['put_down']=each_fairy['put_down'][0]
            _fairy_data['reward_status']=each_fairy['reward_status'][0]

            if '0' != _fairy_data['reward_status']:
                _rewards.append(_fairy_data['serial_id'])
            if '0' != _fairy_data['hp']:
                _fairy.append(_fairy_data)
        return _fairy,_rewards
        
    def __do_battle(self,serial_id,user_id,deck_number='1'):
        _url='fairy_top'
        _content,_header=self.__poster.post(_url)
        _url='fairy_battle'
        _postdata={'no':deck_number,
                   'serial_id':serial_id,
                   'user_id':user_id}
        _list={'your_data':{'name':[],'townlevel':'','gold':'','cp':'','ap':['current','max'],'bc':['current','max'],
                           'free_ap_bc_point':[],'gacha_ticket':[]},'fairy':['serial_id','hp','hp_max']}
        return self.__poster.post(_url,postdata=_postdata,list=_list)
        
    def battle(self):
        for fairy in self.__fairy_list:
            if True:
                logger.info('fight with %s \'s fairy' % (fairy['discoverer_name']))
                self.__do_battle(fairy['serial_id'], fairy['discoverer_id'])
                
    def good(self,serial_id,user_id,dialog='1'):
        _url='battle_good'
        _postdata={'dialog ':dialog,
                   'serial_id':serial_id,
                   'user_id':user_id}
        return self.__poster.post(_url)
                
class guid_fairy(enemy):
        
    def __init__(self,poster):
        self.__poster=poster
        self.__fairy_list,self.__rewards = self.__get_info()

    def __get_info(self):
        _url='guild_top'
        _list={'*'}
        _content,_header=self.__poster.post(_url,postdata={},list=_list)
        return self.__change_list(_content['fairy_select'][0])
        
    def __change_list(self,data):
        _rewards=[]
        _user={}
        for each_user in data['user']:
            _user[each_user['id'][0]]=each_user['name'][0]
        _fairy=[]
        for each_fairy in data['fairy_event']:
            _now_fairy=each_fairy['fairy'][0]
            _fairy_data={}
            _fairy_data['serial_id']=_now_fairy['serial_id'][0]
            _fairy_data['name']=_now_fairy['name'][0]
            _fairy_data['lv']=_now_fairy['lv'][0]
            _fairy_data['hp']=_now_fairy['hp'][0]
            _fairy_data['hp_max']=_now_fairy['hp_max'][0]
            _fairy_data['rare_flg']=_now_fairy['rare_flg'][0]
            _fairy_data['discoverer_id']=_now_fairy['discoverer_id'][0]
            _fairy_data['discoverer_name'] = _user[_fairy_data['discoverer_id']]
            _fairy_data['put_down']=each_fairy['put_down'][0]
            _fairy_data['reward_status']=each_fairy['reward_status'][0]

            if '0' != _fairy_data['reward_status']:
                _rewards.append(_fairy_data['serial_id'])
            if '0' != _fairy_data['hp']:
                _fairy.append(_fairy_data)
        return _fairy,_rewards
        
    def __do_battle(self,serial_id,user_id,deck_number='1'):
        _url='fairy_top'
        _content,_header=self.__poster.post(_url)
        _url='fairy_battle'
        _postdata={'no':deck_number,
                   'serial_id':serial_id,
                   'user_id':user_id}
        _list={'your_data':{'name':[],'townlevel':'','gold':'','cp':'','ap':['current','max'],'bc':['current','max'],
                           'free_ap_bc_point':[],'gacha_ticket':[]},'fairy':['serial_id','hp','hp_max']}
        _content,_header=self.__poster.post(_url,postdata=_postdata,list=_list)
        f=open('D:\\milliondata\\battle','w')
        f.write(_content['*'])
        f.close()
        
    def battle(self):
        for fairy in self.__fairy_list:
            if True:
                logger.info('fight with %s \'s fairy' % (fairy['discoverer_name']))
                self.__do_battle(fairy['serial_id'], fairy['discoverer_id'])
        
if __name__ == '__main__':
    player=Player()
    f=open('D:/area','r')
    player.get_area(f.read())