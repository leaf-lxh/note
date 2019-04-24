<?php

//md5 = 14f9bc405312d4fc13821ace31080ed1
$session = unserialize('a:4:{s:10:"session_id";s:32:"083109466d5df2c2fe3f97d919a2fd91";s:10:"ip_address";s:13:"153.101.68.87";s:10:"user_agent";s:10:"luoxiaohei";s:9:"user_data";s:0:"";}');

$session['session_id']='leaf';
$session['ip_address']="153.101.68.87";
$session['user_agent']='luoxiaohei';

var_dump($session);


?>
