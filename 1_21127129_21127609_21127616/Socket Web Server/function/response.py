import config


class Response:
	def __init__(self, path):

		self.file_buff = ''
		self.status = 200

		# Đây là hàm định hướng path đến nơi lấy thông tin nếu trong request có yêu cầu lấy file 
		# Response đc gọi trong hàm getMethod và postMethod, chuyền vào hàm các path mà client muốn truy cập, hàm sẽ trả về path dẫn đến nơi có file 

		self.ChunkedSend = True			
		if path in ['/','/index.html','/index.html?']: 
			path = config.get_index
			self.ChunkedSend = False
		if path in ['/','/images.html','/images.html?']: 
			path = config.get_images
			self.ChunkedSend = False
		if path in ['/404.html','/404.html?']: 
			path = config.get_404
			self.status = 404		
			self.ChunkedSend = False					
		if path in ['/401.html','/401.html?']: 
			path = config.get_401
			self.status = 401		
			self.ChunkedSend = False
		if path == '/css/style.css':
			path = "/css/style.css"
			self.ChunkedSend = False
		if path == '/css/utils.css':
			path = "/css/utils.css"
			self.ChunkedSend = False 
		if path == '/images/pexels-quang-nguyen-vinh-4544171.jpg':
			path = "/images/pexels-quang-nguyen-vinh-4544171.jpg"
			self.ChunkedSend = False
		if path == '/images/pexels-quang-nguyen-vinh-5118664.jpg':
			path = "/images/pexels-quang-nguyen-vinh-5118664.jpg"
			self.ChunkedSend = False
		if path == '/images/pexels-quang-nguyen-vinh-6136262.jpg':
			path = "/images/pexels-quang-nguyen-vinh-6136262.jpg"
			self.ChunkedSend = False
		if path == '/images/pexels-quang-nguyen-vinh-6877795.jpg':
			path = "/images/pexels-quang-nguyen-vinh-6877795.jpg"
			self.ChunkedSend = False 
		if path == '/avatars/1.png':
			path = "/avatars/1.png"
			self.ChunkedSend = False
		if path == '/avatars/2.png':
			path = "/avatars/2.png"
			self.ChunkedSend = False
		if path == '/avatars/3.png':
			path = "/avatars/3.png"
			self.ChunkedSend = False
		if path == '/avatars/4.png':
			path = "/avatars/4.png"
			self.ChunkedSend = False
		if path == '/avatars/5.png':
			path = "/avatars/5.png"
			self.ChunkedSend = False
		if path == '/avatars/6.png':
			path = "/avatars/6.png"
			self.ChunkedSend = False
		if path == '/avatars/7.png':
			path = "/avatars/7.png"
			self.ChunkedSend = False
		if path == '/avatars/8.png':
			path = "/avatars/8.png"
			self.ChunkedSend = False
		
		


		# Split path into array to get file name and file type
		self.locOf_file = path							
		file_info = path.split('/')[-1].split('.')	 
		self.file_type = file_info[-1]		# Get file type from array   


		#try to open file that provide above, if false, return status code 404 and 404.html
		try:
			if(self.file_buff == ''):
				if(self.ChunkedSend != True):
					self.buffer = open(path[1:],"rb")  
				else:
					self.buffer = open(path[1:].replace("%20"," "),"rb")			# Get data buffer from file    
					
		except:
			self.status = 404
			self.ChunkedSend = False
			self.buffer = open(config.get_404[1:],"rb")

		#make header
		header = ""	
		header += "HTTP/1.1 404 NOT FOUND\n" if(self.status == 404) else "HTTP/1.1 200 OK\n"
		if self.file_type in ["html","txt"]:
			header += 'Content-Type: text/%s\n'%self.file_type
		else:
			if self.file_type in ["png","ico","jpg"]:
				header += 'Content-Type: image/%s\n'%self.file_type
			if self.file_type in ["css"]:
				header += 'Content-Type: text/%s\n'%self.file_type
			
				
		self.header = header
		print(f'-------------------\n [HEADER RESPONSE]\n {header}')

	def makeResponse(self):

		if(self.file_buff != ''):
			content = self.file_buff.encode('utf-8')
		else:
			content = self.buffer.read()

		self.header += "Content-Length: %d\r\n\r\n"%len(content) 
		header = self.header.encode('utf-8') + content + "\r\n".encode('utf-8')   # tạo header response, encode(uft 8) là chuyển nội dung thành dạng uft-8 scheme 
		print(f"-------------------\n [SEND RESPONSE]\n Transfer {self.locOf_file} with normal mode")
		return header

