// client user ip
var_dump($_SERVER['REMOTE_ADDR']);

// server ip (maybe private ip)
var_dump($_SERVER['SERVER_ADDR']);

// server ip (global ip)
$ip = rtrim(`curl inet-ip.info 2>/dev/null`);
var_dump($ip);