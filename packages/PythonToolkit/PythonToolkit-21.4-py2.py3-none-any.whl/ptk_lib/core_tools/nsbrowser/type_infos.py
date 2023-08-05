"""
Module conatinging callables to get info/value string for NSBrowser

format: callable(eng, oname)
"""

def infovalue(eng,oname):
    """
    Used by the namespace browsers info/value column defaults to string 
    representation of object returned by __repr__
    """
    #special cases for builtins
    if oname == '__builtins__.True':
        return 'True'
    if oname == '__builtins__.False':
        return 'False'
    if oname == '__builtins__.None':
        return 'None'
    
    res = eng.evaluate('str('+oname+')')   
    
    #truncate to 
    if len(res)>80:
        res = res[:80]+' ...'
    
    return res

