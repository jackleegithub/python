import os

def application(e, r):
    r('200 ok', [('Content-Type', 'text/html')])
    s =b'<ul>'
    # for key in os.environ.keys():
    #     t = '<li>%s:%s</li>' % (key,os.environ[key])
    #     s = s + bytes(t,encoding='utf-8')

    for key in e.keys():
        t = "<li><span style='color:red;font-weight:800;'>%s:</span>%s" %(key, e[key])
        s = s + t.encode('utf-8')
    s = s + b'</ul>'
    return [s]