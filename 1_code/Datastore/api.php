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

	/**
	*
	*/
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
		$retval='';
		switch($this->furl_function){
			case 'loginUser':
				$retval=$this->datastore->loginUser($this->furl_id,$this->requestVars['password']);
			break;
			case 'addUser':
				$retval=$this->datastore->addUser($this->requestVars['fname'],$this->requestVars['lname'],$this->furl_id,$this->requestVars['password']);
			break;
			case 'getUser':
				$retval=$this->datastore->getUser($this->furl_id,$this->requestVars['authtoken']);
			break;
			case 'addWorkout':
				$retval=$this->datastore->addWorkout($this->requestVars['authtoken'],$this->requestVars['workout_type'],$this->requestVars['distance'],$this->requestVars['workout_time'],$this->requestVars['calories']);
			break;
			case 'getAllWorkout':
				$retval=$this->datastore->getAllWorkout($this->requestVars['authtoken']);
			break;
			case 'getWorkout':
				$retval=$this->datastore->getWorkout($this->requestVars['authtoken'],$this->furl_id);
			break;
			default:
				throw new apiException('function not found',1);
			break;
		}
		return $retval;
	}
}

try{
	$api=new api();
	$results=$api->processRequest();
	echo $results;
}
catch(Exception $e){
	header('HTTP/1.1 '.$e->getHttpCode().' '.$e->getMessage());
} ?>