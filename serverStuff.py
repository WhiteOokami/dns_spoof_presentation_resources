#!/usr/bin/python

# Import modules for CGI handling
import cgi, cgitb

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
user_id = form.getvalue('user_id')
password  = form.getvalue('password')

while True:
	if (user_id != "none" and password !="none"):
		print(user_id)
		print(password)
