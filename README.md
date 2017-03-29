# C.O.R.E.S
    Cross-Origin Resource Exploitation Server

# Cross-Origin Resource Exploitation Server
    This tool leverages a common misconfiguration in CORS that allows Cross-Origin Sharing 
    from all domains with credentials!
    
    The CORS spec disallows the following setting: 
    Access-Control-Allow-Origin: *
    Access-Control-Allow-Credentials: true
    
    A common misconfiguration or work around for this restriction is the following 
    Server side example:
    <? php
    header('Access-Control-Allow-Origin: ' + $_SERVER['HTTP_ORIGIN']);
    header('Access-Control-Allow-Credentias: true');
    
# Usage
    Usage: python cores.py <URL> <OPTIONS>
    Example[1]: python cores.py https://target-site.com/
    Example[2]: python cores.py https://target-site.com/ -m GET -s html -v
    
    Example 1 is the most common, simply supply your target URL and cores will use 
    the HTTP method GET by default.
    
    Example 2 demonstrates the HTTP (-m)ethod and (-s)tyle of the Proof of Concept (PoC) being specified.
    "-s html" will deliver the loot within the HTML page while the latter "-s alert" will diplay the loot
    inside a JavaScript Alert box.

