# Overview

This repo is for creating a [Heroku](https://www.Heroku.com/) python3 Flask application for the purpose of demonstrating how a cross site scripting (XSS) vulnerability
can lead to hijacking accounts and stealing passwords in the very cool [OWASP Juice Shop](https://juice-shop.herokuapp.com/) website.

I have used this to teach application security to development teams at my employment.  The OWASP Juice Shop is an absolutely fantastic site for demonstrating
security vulnerabilities.  It is a modern single page web application using Nodejs and JWTs, and contains a lot of nice security
vulnerabilities that can be chained together to make really cool attacks.  The goal of my demonstration is not just to show single vulnerabilities, but
how  they can be  exploited in practice.  This repository serves as the malicious server that would be used in a real XSS exploit (for testing purposes only, of
course).

The demonstration involves a DOM-based XSS in the OWASP Juice Shop search page.  To exploit it, our malicious website creates a link that promises free
juice if you click it.  Clicking the link triggers an XSS that takes the victim's cookie and sends it to a /recorddata endpoint on our malicious server.
From there, we can hit a /dumpdata endpoint that displays the captured cookies.  The cookies contain JWTs, which when decoded, contain the MD5 hash
of the user password.  Using [Google dorking](https://en.wikipedia.org/wiki/Google_hacking), we invert the MD5 hash to recover the victim's password.

# Prerequisites

You only need a Heroku account to run this, and you can get one for free.  From there, you can deploy this application and it won't cost you a cent.

To learn about Heroku, I strongly recommend reading Dan Nguyen's [Heroku basic flask app](https://github.com/datademofun/Heroku-basic-flask), which
is so much easier to follow than Heroku documentation (I have really struggled with putting Flask on Heroku in the past!!!).

In short, all you need to d is:

* Clone this code from github
* Install heroku toolbelt
* heroku login
* Do the following from the directory containing this repository's source code
    * git init
    * git add .
    * git commit -m "first commit"
    * heroku create
    * git push heroku master


From there, your server should be deployed in a few seconds, and you will be able to perform this demo from it.
In my case, the server name is https://frozen-crag-69213.herokuapp.com (I will delete this later -- but you can deploy your own with this code!)

# The Demo

First head over to the [OWASP Juice Shop](https://juice-shop.herokuapp.com/) and click Login.  From there, you can register.  See Figure below:

![picture alt](https://github.com/ScottContini/juiceshop_xss_example/blob/master/images/01_login_juice.png "Victim registers for an account")




