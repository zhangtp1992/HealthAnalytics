<?php include('datastore.php');

class apiException extends SE1Exception
{
    public function __construct($message, $code) {
        parent::__construct($message,$code);
    }
}

class api
{
	public $requestVars=[];
	public $furl_function='';
	public $furl_id='';
	public $datastore='';
	public $retval=['results'=>''];

	public function __construct(){
		if($_GET['furl_function']=='null'){
			throw new apiException('No function was provided',1);
		}
		$data=file_get_contents('php://input');
		$ct=explode(';',$_SERVER['HTTP_CONTENT_TYPE']);;
		switch(trim($ct[0])){
			case 'application/json':
			case 'text/json':
				$requestVars=json_decode($data,TRUE);
			break;
			default:
				parse_str(trim($data),$requestVars);
			break;
		}
		$this->requestVars=$requestVars;
		if(!empty($_GET)){
			foreach($_GET as $key=>$val){
				switch($key){
					case 'furl_function':
						$this->furl_function=$_GET['furl_function'];
					break;
					case 'furl_id':
						$this->furl_id=$_GET['furl_id'];
					break;
					default:
						$this->requestVars[$key]=$val;
					break;
				}
			}
		}
		$this->__datastoreConnect();
	}

	private function __datastoreConnect(){
		$this->datastore=new datastore();
	}

	public function processRequest(){
		switch($this->furl_function){
			case 'loginUser':
				$this->datastore->loginUser($this->furl_id,$_GET['password'],$_GET['token']);
			break;
			default:
				throw new apiException('function not found',1);
			break;
		}
	}
}

try{
	$api=new api();
	$api->processRequest();
	$api->retval['results']=1;
	echo str_replace('":null','":""',json_encode($api->retval));
}
catch(Exception $e){
	header('HTTP/1.1 '.$e->getHttpCode());
	echo $e->getMessage();
} ?>