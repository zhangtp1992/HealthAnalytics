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
		if(isset($_SERVER['HTTP_AUTHTOKEN'])){$this->requestVars['authtoken']=$_SERVER['HTTP_AUTHTOKEN'];}
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
						#authtoken sent from header takes priority over authtoken sent via other method
						if(($key=='authtoken'&&!isset($_SERVER['HTTP_AUTHTOKEN']))||$key!='authtoken'){
							$this->requestVars[$key]=$val;
						}
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
			case 'addUser':
				$retval=$this->datastore->addUser($this->requestVars['fname'],$this->requestVars['lname'],$this->furl_id,$this->requestVars['password'],$this->requestVars['mi'],$this->requestVars['weight'],$this->requestVars['height'],$this->requestVars['birth_date'],$this->requestVars['gender'],$this->requestVars['waist_size'],$this->requestVars['address1'],$this->requestVars['address2'],$this->requestVars['city'],$this->requestVars['state'],$this->requestVars['zip']);
			break;
			case 'addWorkout':
				$retval=$this->datastore->addWorkout($this->requestVars['authtoken'],$this->requestVars['workout_type'],$this->requestVars['distance'],$this->requestVars['duration'],$this->requestVars['workout_timestamp'],$this->requestVars['calories'],$this->requestVars['comments']);
			break;
			case 'addFood':
				$retval=$this->datastore->addFood($this->requestVars['authtoken'],$this->requestVars['food'],$this->requestVars['serving'],$this->requestVars['meal'],$this->requestVars['food_timestamp'],$this->requestVars['comments']);
			break;
			case 'getFood':
				$retval=$this->datastore->getFood($this->requestVars['authtoken'],$this->furl_id);
			break;
			case 'getFoodAll':
				$retval=$this->datastore->getFoodAll($this->requestVars['authtoken']);
			break;
			case 'getFoodList':
				$retval=$this->datastore->getFoodList($this->requestVars['authtoken']);
			break;
			case 'getFoodUser':
				$retval=$this->datastore->getFoodUser($this->requestVars['authtoken'],$this->furl_id);
			break;
			case 'getHealthStats':
				$retval=$this->datastore->getHealthStats($this->requestVars['authtoken'],$this->requestVars['age'],$this->requestVars['height'],$this->requestVars['weight'],$this->requestVars['waist_size'],$this->requestVars['gender'],$this->requestVars['ethnicity'],$this->requestVars['state']);
			break;
			case 'getUser':
				$retval=$this->datastore->getUser($this->furl_id,$this->requestVars['authtoken']);
			break;
			case 'getUserAll':
				$retval=$this->datastore->getUserAll($this->requestVars['authtoken']);
			break;
			case 'getWorkout':
				$retval=$this->datastore->getWorkout($this->requestVars['authtoken'],$this->furl_id);
			break;
			case 'getWorkoutAll':
				$retval=$this->datastore->getWorkoutAll($this->requestVars['authtoken']);
			break;
			case 'getWorkoutUser':
				$retval=$this->datastore->getWorkoutUser($this->requestVars['authtoken'],$this->furl_id);
			break;
			case 'loginUser':
				$retval=$this->datastore->loginUser($this->furl_id,$this->requestVars['password']);
			break;
			case 'logoutUser':
				$retval=$this->datastore->logoutUser($this->requestVars['authtoken'],$this->furl_id);
			break;
			case 'updateUser':
				$retval=$this->datastore->updateUser($this->requestVars['fname'],$this->requestVars['lname'],$this->furl_id,$this->requestVars['mi'],$this->requestVars['weight'],$this->requestVars['height'],$this->requestVars['birth_date'],$this->requestVars['gender'],$this->requestVars['waist_size'],$this->requestVars['address1'],$this->requestVars['address2'],$this->requestVars['city'],$this->requestVars['state'],$this->requestVars['zip'],$this->requestVars['authtoken']);
			break;
			default:
				throw new apiException('function not found',1);
			break;
		}
		return $retval;
	}
}

#respond with only a "200 OK" response if the request method is "OPTIONS". The client will immediately follow up with a POST/GET/PUT/DELETE request.
#OPTIONS is used to check if the server allows for cross site scripting (Since this API communicates with clients on different servers, this must
#be enabled
if(strtoupper($_SERVER['REQUEST_METHOD'])=='OPTIONS'){exit;}
try{
	$api=new api();
	$results=$api->processRequest();
	echo $results;
}
catch(Exception $e){
	header('HTTP/1.1 '.$e->getHttpCode().' '.$e->getMessage());
} ?>