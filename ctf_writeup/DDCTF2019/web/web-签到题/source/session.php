<?php
include 'Application.php';
class Session extends Application {

    //key建议为8位字符串
    var $eancrykey                  = 'EzblrbNS';
    var $cookie_expiration			= 7200;
    var $cookie_name                = 'ddctf_id';
    var $cookie_path				= '';
    var $cookie_domain				= '';
    var $cookie_secure				= FALSE;
    var $activity                   = "DiDiCTF";


    public function index()
    {
	if(parent::auth()) { //通过此处需要加header  didictf_username: admin
            $this->get_key(); //获取文件../config/key.txt的内容，赋值到$this->eancrykey
            if($this->session_read()) {//可以打印eancrykey, 通过此处验证需要设置cookie:ddctf_id=hash
                $data = 'DiDI Welcome you %s';
                $data = sprintf($data,$_SERVER['HTTP_USER_AGENT']);
                parent::response($data,'sucess');
            }else{
                $this->session_create();
                $data = 'DiDI Welcome you';
                parent::response($data,'sucess');
            }
        }

    }

    private function get_key() {
        //eancrykey  and flag under the folder
        $this->eancrykey =  file_get_contents('../config/key.txt');
    }

    public function session_read() {
        if(empty($_COOKIE)) {
        return FALSE;
        }

        $session = $_COOKIE[$this->cookie_name];//ddctf_id
        if(!isset($session)) {
            parent::response("session not found",'error');
            return FALSE;
        }
        $hash = substr($session,strlen($session)-32); //cookie ddctf_id的值, 如果值超过32位，则取其后32位字符
        $session = substr($session,0,strlen($session)-32);//cookie ddctf_id的值, 如果值超过32位，则取其前len(ddctf_fd)-32位字符

        if($hash !== md5($this->eancrykey.$session)) {//绕过此处需要让ddctf_id的长度超过32，然后md5长度扩展攻击
            parent::response("the cookie data not match",'error');
            return FALSE;
        }
        $session = unserialize($session);//将$session进行反序列化，构造authentication类，设置path


        if(!is_array($session) OR !isset($session['session_id']) OR !isset($session['ip_address']) OR !isset($session['user_agent'])){
            return FALSE;
        }

        if(!empty($_POST["nickname"])) {
            $arr = array($_POST["nickname"],$this->eancrykey);
            $data = "Welcome my friend %s";
            foreach ($arr as $k => $v) {//这里想要让sprintf把enkey扔到data中，需要把nickname设置成%s
                $data = sprintf($data,$v);
            }
            parent::response($data,"Welcome");
        }

        if($session['ip_address'] != $_SERVER['REMOTE_ADDR']) {//需要设置
            parent::response('the ip addree not match'.'error');
            return FALSE;
        }
        if($session['user_agent'] != $_SERVER['HTTP_USER_AGENT']) {
            parent::response('the user agent not match','error');
            return FALSE;
        }
        return TRUE;

    }

    private function session_create() {
        $sessionid = '';
        while(strlen($sessionid) < 32) {
            $sessionid .= mt_rand(0,mt_getrandmax());
        }

        $userdata = array(
            'session_id' => md5(uniqid($sessionid,TRUE)),
            'ip_address' => $_SERVER['REMOTE_ADDR'],
            'user_agent' => $_SERVER['HTTP_USER_AGENT'],
            'user_data' => '',
        );

        $cookiedata = serialize($userdata);
        $cookiedata = $cookiedata.md5($this->eancrykey.$cookiedata);
        $expire = $this->cookie_expiration + time();
        setcookie(
            $this->cookie_name,
            $cookiedata,
            $expire,
            $this->cookie_path,
            $this->cookie_domain,
            $this->cookie_secure
            );

    }
}


$ddctf = new Session();
$ddctf->index();
?>