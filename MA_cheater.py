'''
Created on 2014-1-30

@author: bell
'''
import Connecter

class Client():
    def __init__(self,location):
        
        self.__location=location
        self.__poster=Connecter.poster(location)
        
    def login(self,username,passwd):
        
        _postdata={'login_id':username,
                  'password':passwd
                  }
        _content,_header=self.__poster.post('check_inspection?cyt=1')
        if 'Set-Cookie' in _header:
            self.__cookie=_header['Set-Cookie'].split(',')[1].split(';')[0].lstrip(' ')
            self.__poster.updata_header('Cookie', self.__cookie)
        
        _content,_header=self.__poster.post('login?cyt=1', postdata=_postdata)
        self.__get_configure(_content)
        
    def __get_configure(self,_content):
        data=('party_name')
        import XMLParser
        _parser=XMLParser.XMLParser(_content)
        list=_parser.get_data(data)
        print list['party_name']

if __name__=='__main__':
    MA_client=Client('jp')
    username='belldandyxtq'
    passwd='XtqXds05291224'
    MA_client.login(username, passwd)