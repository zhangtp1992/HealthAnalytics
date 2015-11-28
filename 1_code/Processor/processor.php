<?php include('datastore.php');

#A Custom exception class for generating HTTP error codes
class apiException extends SE1Exception
{
    public function __construct($message, $code) {
        parent::__construct($message,$code);
    }
}

/**
* The url to the API is http://www.ruagetch.edu/se1/api
* The login URL is http://www.rugatech.com/se1/api/loginUser/ntaylor@aps.rutgers.edu?password=123456
* The function in this example is "loginUser".  This is saved to the variable api::furl_function (furl stands for 'Friendly URL' in caes you were wondering).
* The ID in this example is "ntaylor@aps.rutgers.edu". This is saved to the variable api::furl_id.
* All $_POST and $_GET variables (with the exception of the function and the id are saved into the variable array api::requestVars.  Therefore, is does not matter if variables are passed via a POST or GET request. (Not 100% RESTFul, but easier to code).
*/

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

		#This loads non-GET request variables in into api::requestVars
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

		#GET variables are loaded here (with the exception of `furl_function` and `furl_id`
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

	#Connect the API to the Datastore
	private function __datastoreConnect(){
		$this->datastore=new datastore();
	}

	#Call the appropriate datastore method based upon the `furl_function`
	public function processRequest(){
		$retval='';
		switch($this->furl_function){
			case 'loginUser':
				$retval=$this->datastore->loginUser($this->furl_id,$this->requestVars['password']);
			break;
			#for the purposes of the project, `addUser` is completely open.  Anybody can create an account.
			case 'addUser':
				$retval=$this->datastore->addUser($this->requestVars['fname'],$this->requestVars['lname'],$this->furl_id,$this->requestVars['password']);
			break;
			#`get_user` will return an error message if you try to fetch a user other then yourself
			case 'getUser':
				$retval=$this->datastore->getUser($this->furl_id,$this->requestVars['authtoken']);
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
#See SE1Exceptions.php for which HTTP Error Codes are thrown
catch(Exception $e){
	header('HTTP/1.1 '.$e->getHttpCode().' '.$e->getMessage());
} ?>