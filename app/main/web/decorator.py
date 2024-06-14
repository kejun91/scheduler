api_routes = []
webpage_routes = []

def api(path, method):
    '''
    path should be unique
    '''
    def wrapper(func):
        api_routes.append({
            'path':path,
            'func':func,
            'method':method
        })
        return func
    return wrapper
    
def webpage(path):
    '''
    path should be unique
    '''
    def wrapper(func):
        webpage_routes.append({
            'path':path,
            'func':func
        })
        return func
    return wrapper