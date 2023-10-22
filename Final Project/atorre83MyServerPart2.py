import sys
import os
import time
import socket
import csv

'''REFERENCES:
https://docs.python.org/3/library/os.html
https://edstem.org/us/courses/32455/discussion/2738148 - Neil's csv explination
https://towardsthecloud.com/get-absolute-path-python#:~:text=To%20get%20an%20absolute%20path%20in%20Python%20you%20use%20the,working%20directory%20including%20the%20file.
Section 2.7 of the textbook Computer Networks: A Top-Down Approach 8th edition
'''


port = sys.argv[2]
path_to_directory = sys.argv[4]
int_port = int(port)

root_directory = path_to_directory.split('/')

if not os.path.exists("/" + root_directory[1]):
    sys.stderr.write("Error: Root directory does not exist: %s\n" % root_directory[1])
    exit()
if int_port <=0 or int_port > 65535:
    sys.stderr.write("Error: Invalid port number %s\n" % str(int_port))
    exit()
if int_port >= 1 and int_port <= 1023:
    sys.stdout.write("WARNING: WELL-KNOWN PORT\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_ip = "127.0.0.1"
    sys.stdout.write("Welcome socket created: %s, %s\n" % (server_ip, int_port))
    server_socket.bind((server_ip, int_port))
    server_socket.listen(1)

    while True:
        client_socket, client_address = server_socket.accept()
        c_add, c_sock = client_socket.getpeername()
        request = client_socket.recv(1024)
        sys.stdout.write("Connection requested from %s, %s\n" % (c_add, c_sock))
        if request:
            req_parse = request.decode()
            req_line = req_parse.split('\r\n')
            method, file_name, version = req_line[0].split()
            print("FILENAME:")
            print(file_name)
            url = file_name
            name = file_name.split("/")
            file_name = name[-1]

            print("URL:")
            print(url)
            print("FILENAME:")
            print(file_name)

            file_split = file_name.split('.')
            file_ext = file_split[-1]

            mime_types = {"csv": "text/csv", "png": "image/png", "jpg": "image/jpeg", "gif": "image/gif", "zip": "application/zip", "txt": "txt/plain", "html": "text/HTML", "doc": "application/msword", "docx": "applicaiton/vnd.openxmlformats-officedocument.wordpressingml.document"}   
            if file_ext in mime_types:
                file_ext = mime_types[file_ext]

            error_type = 0
            byte_types = ["png", "jpg", "gif", "zip"]    
            txt_types = ["csv", "txt", "html", "doc", "docx"]
            curr_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())

            if not os.path.exists(path_to_directory + url):
                error_type = 1
                status_line = ("HTTP/1.1 404 NOT FOUND\r\n")
                csv_status_line = ("HTTP/1.1 404 NOT FOUND")
                date = ("Date: " + curr_time +"\r\n\r\n")
                headers = (status_line + date)
                response = status_line.encode() + date.encode()
                client_socket.send(response)
                bytes_transmitted = 0
                client_socket.close()
                sys.stdout.write("Connection to %s, %s is closed\n" % (c_add, c_sock))

            elif method != 'GET':
                error_type = 2
                status_line = ("HTTP/1.1 501 NOT IMPLEMENTED\r\n")
                csv_status_line = ("HTTP/1.1 501 NOT IMPLEMENTED")
                date = ("Date: " + curr_time +"\r\n\r\n")
                headers = (status_line + date)
                response = status_line.encode() + date.encode()
                client_socket.send(response)
                bytes_transmitted = 0
                client_socket.close()
                sys.stdout.write("Connection to %s, %s is closed\n" % (c_add, c_sock))

            elif version != "HTTP/1.1":
                error_type = 3
                status_line = ("HTTP/1.1 505 HTTP VERSION NOT SUPPORTED\r\n")
                csv_status_line = ("HTTP/1.1 505 HTTP VERSION NOT SUPPORTED")
                date = ("Date: " + curr_time +"\r\n\r\n")
                headers = (status_line + date)
                response = status_line.encode() + date.encode()
                client_socket.send(response)
                bytes_transmitted = 0
                client_socket.close()
                sys.stdout.write("Connection to %s, %s is closed\n" % (c_add, c_sock))

            if method == 'GET' and error_type == 0:

                file = open(path_to_directory + url, 'rb')
                content = file.read()

                file_size = os.path.getsize(path_to_directory + url)
                last_time = os.path.getmtime(path_to_directory + url)
                gmt_last = time.gmtime(last_time)
                last_mod = time.strftime("%a, %d %b %Y %H:%M:%S GMT", gmt_last)
                curr_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
                status_line = ("HTTP/1.1 200 OK\r\n")
                csv_status_line = ("HTTP/1.1 200 OK")
                content_length = file_size

                headers = status_line
                headers += ("Content-Length: %d\r\n" % file_size)
                headers += ("Content-Type: %s\r\n" % file_ext)
                headers += ("Date: %s\r\n" % curr_time)
                headers += ("Last-Modified: %s\r\n\r\n" % last_mod)

                response = headers.encode() + content
                client_socket.send(response)
                bytes_transmitted = content_length

                client_socket.close()
                sys.stdout.write("Connection to %s, %s is closed.\n" % (c_add, c_sock))

            txtfile = open('atorre83HTTPResponses.txt', 'a', newline = '\n')
            txtfile.write(headers)
            txtfile.close()

            csvfile = open('atorre83SocketOutput.csv', 'a', newline='\n')
            writer = csv.writer(csvfile)
            writer.writerow(["Client request server", "4-Tuple:", server_ip, int_port,
            c_add, c_sock, "Requested URL", url, csv_status_line, "Bytes transmitted:",bytes_transmitted])
            csvfile.close()
