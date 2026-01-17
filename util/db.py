from typing import Self

class DB:
    ''' Singleton database interface.
    '''
    _instance: Self = None

    def __new__(cls):
        '''
        '''
        if cls._instance is None:
            cls._instance = super().__new__(cls)
    
    def new_thread(self):
        '''
        '''
        pass

    def reply_thread(self):
        '''
        '''
        pass

    def get_thread(self):
        '''
        '''
        pass