

def GetTupleFromString(string):
    """
    Take a string like '(6,7,8)' and return the tuple (6,7,8).
    """
    s = string.replace("(","").replace(")","")
    s = s.split(",")
    for num, obj in enumerate(s):
        try:
            obj = int(obj)
        except:
            pass
        s[num] = obj
    return tuple(s)