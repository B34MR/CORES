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
    
    
