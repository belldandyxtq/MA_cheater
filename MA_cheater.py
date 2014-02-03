'''
Created on 2014-1-30

@author: bell
'''

from Player import Player
import Const
import logging

logger = logging.getLogger('MALogger')
class Client():

    def __init__(self, location,username,passwd):
        self.__player = Player(location,username,passwd)
    #log in
    def login(self):
        self.__player.login()
        
    def __get_configure(self, _content):
        list = {'party_name':[]}
        from XMLParser import SAXParser
        #_parser = XMLParser()
        #_parser.start_parse(_content,list)
        #list = _parser.get_data(list)
    def explore(self):
        try:
            #self.__player.explore()
            #self.__player.private_fairy()
            self.__player.guild_fairy()
        except RuntimeError:
            self.relogin()
        #self.__player.fairy()


        
def setlogger(consoleLogger=True,fileLogger=False):
    _formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if fileLogger:
        _fileHandler=logging.FileHandler(filename=getattr(Const,'LOGFILE'))
        _fileHandler.setFormatter(_formatter)
        _fileHandler.setLevel(getattr(Const,'NOW'))
        logger.addHandler(_fileHandler)
    if consoleLogger:
        _consoleHandler=logging.StreamHandler()
        _consoleHandler.setFormatter(_formatter)
        _consoleHandler.setLevel(getattr(Const,'NOW'))
        logger.addHandler(_consoleHandler)
    
if __name__ == '__main__':
    setlogger()

    MA_client = Client('jp',username,password)
    MA_client.login()
    MA_client.explore()
