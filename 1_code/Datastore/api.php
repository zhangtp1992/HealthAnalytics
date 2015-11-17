<?php include('datastore.php');

class apiException extends Exception
{
    public function __construct($message, $code = 0, Exception $previous = null) {
        parent::__construct($message, $code, $previous);
    }
}

class api
{
	public $requestVars=[];
	public $furl_function='';
	public $furl_id='';
	public $datastore='';

	public function __construct(){
		$data=file_get_contents('php://input');
		switch($_SERVER['HTTP_CONTENT_TYPE']){
			case 'application/json':
				$requestVars=json_decode($data,TRUE);
			break;
			default:
				parse_str(trim($data),$requestVars);
			break;
		}
		$this->requestVars=$requestVars;

		if($_GET['furl_function']=='null'){
			throw new apiException('No function was provided',1);
		}
		$this->furl_function=$_GET['furl_function'];
		$this->furl_id=$_GET['furl_id'];
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
				throw new apiException('function not found');
			break;
		}
	}
}

try{
	$api=new api();
	$api->processRequest();
	echo 'good';
}
catch(apiException $e){
	print_r($e);
	//header("HTTP/1.1 404 Not Found");
	//echo $e->getMessage();
	//exit;
}
catch(datastoreException $e){
	print_r($e);
} ?>
