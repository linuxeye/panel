import os, json
def readfile(filename, mode = 'r'):
    if not os.path.exists(filename):
        return False
    fp = open(filename, mode)
    f_body = fp.read()
    fp.close()
    return f_body

def writefile(filename, body, mode = 'w+'):
    try:
        fp = open(filename, mode);
        fp.write(body)
        fp.close()
        return True
    except:
        return False
