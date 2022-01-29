#!C:\Users\oracledba\AppData\Local\Programs\Python\Python39\python
from wsgiref.handlers import CGIHandler
from app import app

print("Content-type: text/html\n")
CGIHandler().run(app)