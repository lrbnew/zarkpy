#coding=utf-8
from Decorator import Decorator
import site_helper as sh

class Orderby(Decorator):
    ''' decorator = [
        ('Orderby',{'orderby':'{$primary_key} desc'}),
    ]
    '''

    test_me = True

    def all(self, env=None):
        assert(isinstance(self.arguments.orderby, str))
        env = sh.deepCopy(env) if env is not None else {}
        if not env.has_key('orderby') and self.arguments.orderby:
            env['orderby'] = self.arguments.orderby
        return self.model.all(env)
