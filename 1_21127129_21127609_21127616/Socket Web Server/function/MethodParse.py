import socket
import config
from function.response import *

#Get request from client
def getRequest(client):
	request = ''
	client.settimeout(1) # đây là hàm đặt giá trị thời gian request có liên quan đến TCP, nghĩa là client sẽ gửi request đến client trong 1s, nếu timeout có nghĩa là dữ liẹu bị mất hoặc chưa đc gửi 
	
	try:
		#receive request
		request = client.recv(1024).decode()  #hàm này là để chuyển từ binary sang string, thường thì data đc gửi dưới dạng binary nên phải chuyển về string cho ta dễ xử lý 
		while (request):
			request += client.recv(1024).decode()  #dùng vòng while là để lấy hết nột dung request, có thể request sẽ nhiều hơn 1024 kí tự 
	except socket.timeout:
		#if timedout
		if not request:
			print("-------------------\n [SERVER]\n No request from client")
	finally:
		#parse the request for better using
		return RequestParse(request)

class RequestParse:
	def __init__(self, request):  
		#print(request)
		requestArray = request.split("\n")  #hàm split() này là hàm sẽ tách văn bản thành những đoạn nhỏ dựa trên dấu xuống dòng, nghĩa một đoạn trong đó sẽ tương ứng vs 1 dòng trong content request và t/u vs requestArray[0],... 
		#print(requestArray)
		if request == "":
			self.empty = True	#if there is no request content
		else:
			self.empty = False
			self.method = requestArray[0].split(" ")[0]		#get method , hàm này có nghĩa là ta sẽ chia đoạn dòng 1 trong content cx chính là header thành các đoạn nhỏ t/u vs từng array dựa trên dấu cách, aray[0] này có thể là "GET" hoặc là "POST"    
			self.path = requestArray[0].split(" ")[1]		#get path   
			self.content = requestArray[-1]					#get request content
		
		

#POST Method Parser
def postMethod(client, request):
	#scan login content or return info.html or return 404.html
	# Đây là hàm để check password và username, nếu muốn đến images.htlm và cái psw và user nhập đúng thì lập tức đưa đến images.html 
	# hàm sendall là để chờ đến khi data đc gửi đi toàn bộ, còn .endcode() là hàm trả về phiên bản chuỗi đã đc mã hóa của chuỗi ban đầu 
	# "HTTP/1.1 301 MOVED PERMANENTLY\nLOCATION: /images.html\n" này tương đương với việc di chuyển đến page images.html.


	if(request.path in ['/images.html?','/images.html'] and request.content == "Username=%s&Password=%s"%(config.username,config.password)):
		client.sendall("HTTP/1.1 301 MOVED PERMANENTLY\nLOCATION: /images.html\n".encode('utf-8'))
		client.sendall(Response("/html/images.html").makeResponse())
		f = open('block.txt',"w")
		f.write("True");
		f.close();
		return
	else:
		client.sendall("HTTP/1.1 301 MOVED PERMANENTLY\nLOCATION: /401.html\n".encode('utf-8'))
		client.sendall(Response("/html/401.html").makeResponse())
		return



#GET method parser
def getMethod(client, request):

	#if not "GET" method, abort 
	if request.method != 'GET':
		return

	f = open('block.txt',"r")
	check = f.read();
	f.close()
	#print(check)

	#Block access to page if not access via login form
	if(check == "False"):
		if (request.path in ['/images.html','/images.html?']):
			request.path = config.get_401
		# Nếu truy cập vào images.html mà ko qua đăng nhập thì đưa đến page 401 


	f = open('block.txt',"w")
	f.write("False")
	f.close()

	#Return to homepage first time connect
	if request.path in ['/','/index.html?']:
		request.path = config.get_index
	

	
	
	#input the file path to send to client
	client.sendall(Response(request.path).makeResponse())
	print(f"-------------------\n [SEND RESPONSE]\n Package for {Response(request.path).locOf_file} sent")