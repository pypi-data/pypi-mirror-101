*XRZZ* HTTP Request

# Description

     Just a simple module for HTTP Request 

     supports : {

     	 1: GET,
     	 2: POST 
     	 
     }

# Todo

    Accept Cookies
    Persistent Connection to server
    Auto Encode url 
    proxy support
    Auto Redirect facility
	PUT; PATCH; TRACE; CONNECT
	optimization needed

# Supports

	GET, POST	

# Installation

	till now it doesn't need any external modules
	
	pip install xrzz

# Usage 

	import xrzz

	a = xrzz.http("get", 
			url="https://httpbin.org/get", 
			headers={"user-agent": "Xrzz/v1"},
			tls=True)
	print(a.body())


	# output (Bytes)

			b'{\n"args": {},\n"headers": {\n"Host": "httpbin.org",\n "User-Agent": "Xrzz/v1", \n
			"X-Amzn-Trace-Id": "Root=1-606b416e-79346cf934ed2d6f4aa2cbf7"\n  },\n  "origin": "45.103.157.9", \n 
			"url": "https://httpbin.org/get"\n}\n'

			Usually it returns in bytes 

	# output (decoded)

			{
			  "args": {},
			  "headers": {
			    "Host": "httpbin.org",
			    "User-Agent": "Xrzz/v1",
			    "X-Amzn-Trace-Id": "Root=1-606b416e-79346cf934ed2d6f4aa2cbf7"
			  },
			  "origin": "45.103.157.9",
			  "url": "https://httpbin.org/get"
			}


	print(a.head() 

	# output (dict)

			{
				'Date': 'Mon, 05 Apr 2021 17:06:13 GMT', 
				'Content-Type': 'application/json', 
				'Content-Length': '242', 
				'Connection': 'close', 
				'Server': 'gunicorn/19.9.0', 
				'Access-Control-Allow-Origin': '*', 
				'Access-Control-Allow-Credentials': 'true'
			}

# Whats new

	POST METHOD 

# Version 
	
	 v0.1.3
