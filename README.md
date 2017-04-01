# C.O.R.E.S ![Supported Python versions](https://img.shields.io/badge/python-2.7-blue.svg)
    CORES v1.03312017
    Description:Cross-Origin Resource Exploitation Server.
    Created by: Nick Sanzotta/@Beamr
    Contribution thanks to Bill Harshbarger
    
    This tool 'cores.py' will launch a Python SimpleHTTPServer configured with 
    HTML & JavaScript code to execute a CORS Proof of Concept (PoC) vulnerability.
    At a minimum the user will need to supply a URL vulnerable to excessive CORS along 
    with the correct HTTP (-m)ethod.
    
    Optionally, the user has the ability to (-a) Autolaunch FireFox and execute the payload.
	
# Overview:
    The CORS spec denies the header Access-Control-Allow-Origin (ACAO) to be configured with 
    '*' while allowing Access-Control-Allow-Credential (ACAC) set to 'true'.
    Example: (NOT Allowed!)
	Access-Control-Allow-Origin: *
	Access-Control-Allow-Credentials: true
	
    A commonly found misconfiguration or work around for this restriction is the following.
    Example: (Insecure Work Around, Shares with any domain with credentials!)
	<? php 
	header("Access-Control-Allow-Origin: ".$_SERVER["HTTP_ORIGIN"]);
	header("Access-Control-Allow-Credentials: true");

# Installation:
	# git clone https://github.com/NickSanzotta/CORES.git
	# cd CORES/cores/
	# python cores.py
	
# Usage:
	usage: cores.py cores.py <URL> <OPTIONS>
		Example: python cores.py https://site.com/
		Example: python cores.py https://site.com/ -m POST -p 8080 -c -s alert --verbose --auto

		 [-m, Define HTTP request method ex: -m POST]
		 [-p, Define HTTP Server port ex: -p 8080]

		 [-c, Sets "Access-Control-Allow-Credentials: true" ex: -c]
		 [-a, Auto-launches FireFox to automatically visit destination server.]
		 [-s, Select Log style ex: JavaScript Alert / Inner HTML ]


	 None

	optional arguments:
	  -h, --help            show this help message and exit
	  -c, --creds           Sets "Access-Control-Allow-Credentials: true"
	  -a, --auto            Enables FireFox to auto-launch.
	  -v, --verbose         Turn on Verbosity (Displays JavaScript code in STDOUT)

	 URL options:
	  URL [http://site.com/]
				Define vulnerable CORS targert URL ex: https://site.com/
	  -m [GET]              Define HTTP request method [GET, HEAD, POST] ex: -m POST
	  -p [80]               Define HTTP Server Port ex: -p 8080

	 Log style options:
	  -s [alert, html]      ex: -s html   Displays logs in generated HTML.
				ex: -s alert  Displays logs in JavaScript Alert function.

