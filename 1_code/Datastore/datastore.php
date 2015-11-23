<?php include('SE1Exception.php');

class driver extends PDO
{
	function __construct(){
		try{
			parent::__construct('mysql:host=localhost;dbname=se1;charset=UTF8','se1','dfj59jnah19jmdig');
			$this->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
		}
		catch(PDOException $e){
			throw new Exception($e->getMessage());
		}
	}
}

class DatastoreException extends SE1Exception
{
    public function __construct($message, $code) {
        parent::__construct($message, $code);
    }
}

class datastore
{
	public $db;
	public $authenticatedUser=[];

	public function __construct(){
		try{
			$this->db=new driver();
		}
		catch(Exception $e){
			throw new DatastoreException('Unable to connect to database',2);
		}
	}

	private function __logError($error,$func){
		$pstmt=$this->db->prepare('INSERT INTO datastore_errors (error,func) VALUES (?,?)');
		$pstmt->execute([$error,$func]);
	}

	private function __authenticateUser($token){
		try{
			$pstmt=$this->db->prepare('SELECT person FROM session WHERE sessid=?');
			$pstmt->execute([$token]);
			if($pstmt->rowCount()==1){
				$rs=$pstmt->fetch(PDO::FETCH_ASSOC);
				$this->authenticatedUser=$rs;
			}
			else{throw new DatastoreException('User is not authenticated',3);}
		}
		catch(PDOException $e){throw new DatastoreException('ERROR, unable to authenication user',2);}

	}

	public function addUser($fname,$lname,$email,$passwd){
		if(empty($fname)){throw new DatastoreException('You must provide the First Name',5);}
		if(empty($lname)){throw new DatastoreException('You must provide the Last Name',5);}
		if(empty($email)){throw new DatastoreException('You must provide the E-Mail Address',5);}
		if(empty($passwd)){throw new DatastoreException('You must provide the Password',5);}
		try{
			$pstmt=$this->db->prepare('INSERT INTO people SET fname=?, lname=?, email=?, passwd=?');
			$passwd=password_hash($passwd, PASSWORD_BCRYPT, ['cost'=>11]);
			$pstmt->execute([$fname,$lname,$email,$passwd]);
			return('{"results":"User successfully created"}');
		}
		catch(PDOException $e){
			$this->__logError($e->getMessage(),__FUNCTION__);
			if($e->errorInfo[1]==1062){$txt='This email address already exists';$code=4;}
			else{$txt='Unable to create user';$code=2;}
			throw new DatastoreException($txt,$code);
		}
	}

	public function loginUser($email,$password){
		$string = bin2hex(openssl_random_pseudo_bytes(10));
        $length=32;
        $chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
        $authtoken='';
        while(strlen($authtoken)<$length){
            $authtoken.=$chars[mt_rand(0,strlen($chars))];
        }
		$pstmt=$this->db->prepare('SELECT pkey,passwd FROM people WHERE email=? LIMIT 1');
		try{
			$pstmt->execute([$email]);
			if($pstmt->rowCount()<1){
				throw new DatastoreException('E-Mail Address not found',1);
			}
			$rs=$pstmt->fetch(PDO::FETCH_ASSOC);
			if(!password_verify($password, $rs['passwd'])){
				throw new DatastoreException('ERROR, Incorrect password',3);
			}
			$pstmt=$this->db->prepare('INSERT INTO session (authtoken,person) VALUES (?,?)');
			$pstmt->execute([$authtoken,$rs['pkey']]);
			return('{"authtoken":"'.$authtoken.'"}');
		}
		catch(PDOException $e){
			$this->__logError($e->getMessage(),__FUNCTION__);
			throw new DatastoreException('Unable to login',2);
		}
	}
}