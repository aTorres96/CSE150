import sys
import os
import time

if len(sys.argv) != 5:
    sys.stderr.write("Input Error. Usage: -p <port#> -d <path-to-file>\n")
    exit()

port = sys.argv[2]
path_to_directory = sys.argv[4]
file_path = os.path.dirname(path_to_directory)
sys.stdout.write("%s: entered port number, %s: entered root directory path\n" % (port, file_path))

common_port = int(port)

if common_port <=0 or common_port > 65535:
    sys.stderr.write("Error: Invalid port number %s\n" % str(common_port))
    exit()

root_directory = path_to_directory.split('/')
file_split = root_directory[-1].split('.')
file_ext = "html"

if not os.path.exists("/" + root_directory[1]):
    sys.stderr.write("Error: Root directory does not exist: %s\n" % root_directory[1])
    exit()

mime_types = {"csv": "text/csv", "png": "image/png", "jpg": "image/jpeg", "gif": "image/gif", "zip": "application/zip", "txt": "txt/plain", "html": "text/HTML", "doc": "application/msword", "docx": "applicaiton/vnd.openxmlformats-officedocument.wordpressingml.document"}   
if file_ext in mime_types:
    file_ext = mime_types[file_ext]

if common_port >= 1 and common_port <= 1023:
    sys.stdout.write("WARNING: WELL-KNOWN PORT\n")


file = open(path_to_directory + "/HelloWorld.html", 'rt')

content = file.read()

file_size = os.path.getsize(path_to_directory + "/HelloWorld.html")
last_time = os.path.getmtime(path_to_directory + "/HelloWorld.html")
gmt_last = time.gmtime(last_time)
last_mod = time.strftime("%a, %d %b %Y %H:%M:%S GMT", gmt_last)
curr_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())


file.close()
sys.stdout.write("HTTP/1.1 200 OK\r\n")
sys.stdout.write("Content-Length: %d\r\n" % file_size)
sys.stdout.write("Content-Type: %s\r\n" % file_ext)
sys.stdout.write("Date: %s\r\n" % curr_time)
sys.stdout.write("Last-Modified: %s\r\n\r\n" % last_mod)

sys.stdout.write(content)

sys.exit()