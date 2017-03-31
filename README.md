# C.O.R.E.S
    CORES v1.03312017
    Description:Cross-Origin Resource Exploitation Server.
    Created by: Nick Sanzotta/@Beamr
    Contribution thanks to Bill Harshbarger

# Usage
    usage: cores.py cores.py <URL> <OPTIONS>
	Example: python cores.py https://site.com/
	Example: python cores.py https://site.com/ -m GET -p 8080 -s alert -v -a

         [-m, Define HTTP request method ex: -m POST]
         [-p, Define HTTP Server port ex: -p 8080]
         [-a, Auto-launches FireFox to automatically visit destination server.]

         [-s, Define Log style ex: JavaScript Alert / Inner HTML ]
    
    optional arguments:
    -h, --help            show this help message and exit
    -a                    Enables FireFox to auto-launch.
    -v, --verbose         Turn on Verbosity

    URL options:
    URL [http://site.com/]
                          Define vulnerable CORS targert URL ex: https://site.com/
    -m [GET]              Define HTTP request method [GET, HEAD, POST] ex: -m POST
    -p [80]               Define HTTP Server Port ex: -p 8080

    Log style options:
    -s [alert, html]      ex: -s html   Displays logs in generated HTML.
                          ex: -s alert  Displays logs in JavaScript Alert function.


