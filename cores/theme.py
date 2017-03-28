import os
#Theme v1.03282017

class colors:
   white = "\033[1;37m"
   normal = "\033[0;00m"
   red = "\033[1;31m"
   blue = "\033[1;34m"
   green = "\033[1;32m"
   lightblue = "\033[0;34m"

def banner(app, version, author, contributors):
	banner = colors.red + '\n' + app + version \
	+ colors.normal + '\n Description:' + colors.red + 'C' + colors. normal + 'ross-'+ colors.red + 'O' + colors. normal + 'rigin ' + colors.red + 'R' + colors. normal + 'esource ' + colors.red + 'E' + colors. normal + 'xploitation ' + colors.red + 'S' + colors. normal + 'erver.' + '\n'\
  + colors.normal + ' Created by: ' + author + '\n'\
  + colors.normal + ' Contributors: ' + contributors + '\n'\
	+ colors.normal + ' ' + '*' * 79 +'\n' + colors.normal
	print(banner)

def blue(symbol):
  blue_info = ' [' + colors.blue + symbol + colors.normal + '] ' + colors.normal
  return str(blue_info)

def green(symbol):
  green_info = ' [' + colors.green + symbol + colors.normal + '] ' + colors.normal
  return str(green_info)

def red(symbol):
  red_bang = ' [' + colors.red + symbol + colors.normal + '] ' + colors.normal
  return str(red_bang)

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
