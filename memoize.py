# Stolen from Stack Overflow (http://goo.gl/1lqyD)
def memo(func):
    cache = {}
    @ wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap