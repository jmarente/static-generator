# -*- condig: utf-8 -*-

class Singleton(type):
    '''
    @brief Clase singleton sacada de la wikipedia
    '''
    def __init__(cls, name, bases, dct):
        '''
        @brief Constructor
        '''
        cls.__instance = None
        type.__init__(cls, name, bases, dct)

    def __call__(cls, *args, **kw):
        '''
        @brief funcion call
        '''
        if cls.__instance is None:
            print('setting instance')
            cls.__instance = type.__call__(cls, *args, **kw)
        return cls.__instance
