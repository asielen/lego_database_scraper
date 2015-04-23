__author__ = 'http://stackoverflow.com/questions/13512391/to-count-no-times-a-function-is-called'


from functools import wraps

def counter(func):
    @wraps(func)
    def tmp(*args, **kwargs):
        tmp.count += 1
        return func(*args, **kwargs)
    tmp.count = 0
    return tmp