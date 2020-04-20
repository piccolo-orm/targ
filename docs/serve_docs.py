#!/usr/bin/env python
from livereload import Server, shell


server = Server()
server.watch("src/", shell("make html"))
server.serve(root="_build/html")
