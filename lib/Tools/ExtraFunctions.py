

def GetTupleFromString(string):
    s = string.replace("(","").replace(")","")
    s = s.split(",")
    for num, obj in enumerate(s):
        try:
            obj = int(obj)
        except:
            pass
        s[num] = obj
    return tuple(s)