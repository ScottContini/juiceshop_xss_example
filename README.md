# Overview

This repo is for creating a [Heroku](https://www.Heroku.com/) python3 Flask application for the purpose of demonstrating how a cross site scripting (XSS) vulnerability
can lead to stealing user passwords in the [OWASP Juice Shop](https://juice-shop.herokuapp.com/) website.

I have used this to teach application security to development teams.  The OWASP Juice Shop is an absolutely fantastic site for demonstrating
security vulnerabilities.  It is a modern single page web application using Nodejs and JWTs, and contains a lot of nice security
vulnerabilities that can be chained together to make really cool attacks.  The goal of my demonstration is not just to show single vulnerabilities, but
how  such vulnerabilities are  exploited in practice.  This repository serves as the malicious server that would be used in a real XSS exploit (for demonstration purposes only, of
course).

The demonstration involves a DOM-based XSS in the OWASP Juice Shop product search page.  To exploit it, our malicious website creates a link that promises free
juice if you click it.  Clicking the link triggers an XSS that takes the victim's cookie and sends it to a /recorddata endpoint on our malicious server.
From there, we can hit a /dumpdata endpoint to display the captured cookies.  The cookies contain JWTs, which when decoded, contain the MD5 hash
of the user password.  Using [Google dorking](https://en.wikipedia.org/wiki/Google_hacking), we invert the MD5 hash to recover the victim's password.

# Prerequisites

You only need a Heroku account to run this, and you can get one for free.  From there, you can deploy this application and it won't cost you a cent.

To learn about Heroku, I strongly recommend seeing Dan Nguyen's [Heroku basic flask app](https://github.com/datademofun/Heroku-basic-flask), which
is so much easier to follow than Heroku documentation (I have really struggled with putting Flask on Heroku in the past!!!).

In short, all you need to do is:

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
In my case, the server name is https://frozen-crag-69213.herokuapp.com (I will delete my demo server later, so be sure to deploy your own!)

# The Demo

First head over to the [OWASP Juice Shop](https://juice-shop.herokuapp.com/) and click Login.  From there, you can register.  See Figure below:

![picture alt](https://github.com/ScottContini/juiceshop_xss_example/blob/master/images/01_login_juice.png "Victim registers for an account")


From there you create the account of your victim user:

![picture alt](https://github.com/ScottContini/juiceshop_xss_example/blob/master/images/02_create_account.png "Victim creates an account")


Next, the victim logs in:

![picture alt](https://github.com/ScottContini/juiceshop_xss_example/blob/master/images/03_victim_login.png "Victim logs in")

All is fine and dandy, until somebody tells the victim of a website that offers free juice to OWASP Juice Shop customers.  What could be better!
The victim rushes to the site (for our temporary deployment, link is: https://frozen-crag-69213.herokuapp.com/freejuice):

![picture alt](https://github.com/ScottContini/juiceshop_xss_example/blob/master/images/04_freejuice.png "Victim logs in")

Upon clicking the link, the DOM-based XSS is triggered.  A nontechnical user would likely not understand that a script has executed from the malicious site.
In fact, in this case, the script has taken the victim's cookie and sent it to the malicious website.  The malicious website has a /recorddata endpoint
that records the cookie in a temporary file (a more serious implementation would use a database).

![picture alt](https://github.com/ScottContini/juiceshop_xss_example/blob/master/images/05_link_clicked.png "A script has executed in victim's browser")

Our malicious server also has a /dumpdata endpoint for displaying all the captured cookies.


![picture alt](https://github.com/ScottContini/juiceshop_xss_example/blob/master/images/06_retrieve_cookie.png "We have the victim's cookie!")

Inside the cookie is a JWT.  Let's copy that JWT into our clip board (eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6OSwiZW1haWwiOiJoYXBsZXNzX3ZpY3RpbUBtYWlsaW5hdG9yLmNvbSIsInBhc3N3b3JkIjoiNzA0OTU0OGExMWNhMWQwOGQwMTdkMjQyOWJiMDRhM2IiLCJjcmVhdGVkQXQiOiIyMDE4LTA2LTE2IDA1OjAzOjIzLjA0NyArMDA6MDAiLCJ1cGRhdGVkQXQiOiIyMDE4LTA2LTE2IDA1OjAzOjIzLjA0NyArMDA6MDAifSwiaWF0IjoxNTI5MTI1NDc5LCJleHAiOjE1MjkxNDM0Nzl9.SEeygolhgMsMor0VRJDAL1pg5FGG5m_TUobAgVcaq8OmnZNB8-HfoPGnGj6ZVOBgCJgqEv-AnVHkX4zq11pgZNlbyZcMiEZ0zPpNpiJDejZc047USw5NGeUp-FkUcJv7JgBSqlfHyoNhTepiwXsPgy65tuFRv3NSWEJ_0uUg0Gk for this demo):

![picture alt](https://github.com/ScottContini/juiceshop_xss_example/blob/master/images/07_copy_cookie.png "Copy the JWT")

And now head over to [jwt.io](https://jwt.io/) where we can paste the token in and decode it:

![picture alt](https://github.com/ScottContini/juiceshop_xss_example/blob/master/images/08_jwt_decoded.png "The token decoded")

Amazing!  The username and password are in the cookie.  But that's not the real password, so what is it?  Let's Google it:

![picture alt](https://github.com/ScottContini/juiceshop_xss_example/blob/master/images/09_google_dorking.png "The token decoded")

And clicking the first link, we find out that it was the MD5 hash of the password.  The real password is revealed in the link:

![picture alt](https://github.com/ScottContini/juiceshop_xss_example/blob/master/images/10_get_password.png "The token decoded")

There are lots of other goodies in the OWASP Juice Shop that are fun to demonstrate, so get over there and check it out!





