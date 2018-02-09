# xy2d, d2xy, and rot are based on code from
# https://en.wikipedia.org/wiki/Hilbert_curve
# The use of the hilbert curve for plotting
# IP network or address utilization comes
# from xkcd.com/195

# Note: N is the size of 1 of the dimensions (e.g. 2, 4, 8, 16)
#
# Hilbert curve orders
# 1: 4 points  (2x2)  n=2
# 2: 16 points (4x4)  n=4
# 3: 64 points (8x8)  n=8
# 4: 256 points (16x16)  n=16
# x: 2^(2x)
#

import sys

def xy2d(n, x, y):
    d = 0
    s = n / 2
    while s > 0:
        rx = (x & s) > 0
        ry = (y & s) > 0
        #print n, d, s, x, y, rx, ry
        d += s * s * ((3 * rx) ^ ry)
        x, y = rot(s, x, y, rx, ry)
        s /= 2
    return d

def rot(n, x, y, rx, ry):
    if ry == 0:
        if rx == 1:
            x = n - 1 - x
            y = n - 1 - y
        x, y = y, x
    return x, y

def d2xy(n, d):
    t = d
    s = 1
    x = 0
    y = 0
    while s < n:
        rx = 1 & (t/2)
        ry = 1 & (t ^ rx)
        x, y = rot(s, x, y, rx, ry)
        x += s * rx
        y += s * ry
        t /= 4
        s *= 2
    return x, y

def testgrid(n):
    for x in range(n):
        for y in range(n):
            print "%4i" % (xy2d(n,y,x)),
        print
def testlist(n):
    for x in range(n*n):
        print x, d2xy(n, x)

def test():
    testgrid(4)
    testlist(4)

def testhtml(n):
    print "<html><head><title>test html</title>"
    print "<style>td {width:3.5em; height:3.5em; background: #ccc; text-align:center}</style>"
    print "</head><body>"
    print "<table>"
    for x in range(n):
        print " <tr>"
        for y in range(n):
            d = xy2d(n,y,x)
            c = "white" if d < 128 else "black"
            print '  <td style="background: #%02x%02x%02x; color: %s;">%i</td>' % (d,d,d,c,d)
        print " </tr>"
    print "<table>"
    print "</body></html>"

def testhtml2(n, b):
    c = 0
    #colors = ["red", "blue", "green", "yellow"]#, "cyan", "magenta", "white", "black"]
    colors = ["#f88", "#88f", "#8f8", "#ff0"]
    colors = ["#f00", "#00f", "#0f0", "#dd0"]
    print "<html><head><title>test html</title>"
    print "<style>td {width:3.5em; height:3.5em; background: #ccc; text-align:center}</style>"
    print "</head><body>"
    print "<table>"
    for x in range(n):
        print " <tr>"
        for y in range(n):
            d = xy2d(n,y,x)
            c = d / b
            color = colors[c % len(colors)]
            print '  <td style="background: %s;">%i</td>' % (color,d)
        print " </tr>"
    print "<table>"
    print "</body></html>"

def testhtml3(n):
    c = 0
    b = 21
    sub = 2
    #colors = ["red", "blue", "green", "yellow"]#, "cyan", "magenta", "white", "black"]
    colors = ["red", "blue", "green", "yellow", "cyan", "magenta", "white", "black"]
    #colors = ["red", "blue", "green", "yellow", "cyan", "magenta", "white"]
    #colors = ["red", "blue", "green", "yellow", "cyan", "magenta"]
    #colors = ["#f88", "#88f", "#8f8", "#ff0"]
    #colors = ["#f88", "#88f", "#8f8"]
    colors = ["#f88", "#88f"]
    #colors = ["#fee", "#eef", "#efe", "#ffd"]
    #colors = ["#f00", "#00f", "#0f0", "#dd0"]
    #colors = ["white"]
    print "<html><head><title>test html</title>"
    print "<style>td {width:3.5em; height:3.5em; background: #ccc; text-align:center;border: 2px solid black;} table {border-collapse: collapse;} td.nor {border-right-style: hidden;} td.not {border-top-style: hidden}</style>"
    print "</head><body>"
    print "<table>"
    for y in range(n):
        print " <tr>"
        for x in range(n):
            d = xy2d(n,x,y)
            c = (d-sub) / b
            color = colors[c % len(colors)]
            class_ = []
            if d < 255:
                nextx, nexty = d2xy(n, d+1)
                if nexty == y and nextx == x + 1:
                    class_.append('nor')
                if nextx == x and nexty == y - 1:
                    class_.append('not')
            if d > 0:
                nextx, nexty = d2xy(n, d-1)
                if nexty == y and nextx == x + 1:
                    class_.append('nor')
                if nextx == x and nexty == y - 1:
                    class_.append('not')
            if len(class_):
                class_ = 'class="%s"' % " ".join(class_)
            else:
                class_ = ""
            #class_ = ""
            #print '  <td %s style="background: %s;">%i</td>' % (class_, color,d)
            print '  <td %s style="background: %s;"> </td>' % (class_, color)
        print " </tr>"
    print "<table>"
    print "</body></html>"

def testpng():
    import Image
    i = Image.new("RGB", (256,256))
    for y in range(256):
        for x in range(256):
            d = xy2d(256,x,y)
            i.putpixel((x,y),(d / 256, d % 256, (d * 4) % 256))
    i.save("test.png")

#test()
#testhtml2(16, 2)
#testhtml3(16)
#testhtml(16)
testpng()
