<?php include('SE1Exception.php');

class driver extends PDO
{
	public $error;

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

	public function addUser($token,$fname,$lname,$email,$passwd){
		try{
			$this->__authenticateUser($token);
			$pstmt=$this->db->prepare('INSERT INTO people SET fname=?, lname=?, email=?, passwd=?');
			$passwd=password_hash($passwd, PASSWORD_BCRYPT, ['cost'=>11]);
			$pstmt->execute([$fname,$lname,$email,$passwd]);
		}
		catch(PDOException $e){
			$this->__logError($e->getMessage(),__FUNCTION__);
			if($e->errorInfo[1]==1062){$txt='This email address already exists';$code=4;}
			else{$txt='Unable to create user';$code=2;}
			throw new DatastoreException($txt,$code);
		}
		catch(DatastoreException $e){
			throw new DatastoreException($e->getMessage(),$e->getCode());
		}
	}

	public function loginUser($email,$password,$token){
		$pstmt=$this->db->prepare('SELECT pkey,passwd FROM people WHERE email=? LIMIT 1');
		try{
			$pstmt->execute([$email]);
			if($pstmt->rowCount()<1){
				throw new DatastoreException('E-Mail Address not found',1);
			}
			else{
				$rs=$pstmt->fetch(PDO::FETCH_ASSOC);
				if(!password_verify($password, $rs['passwd'])){
					throw new DatastoreException('ERROR, Invalid password',3);
				}
			}
			$pstmt=$this->db->prepare('INSERT INTO session (sessid,person) VALUES (?,?)');
			$pstmt->execute([$token,$rs['pkey']]);
		}
		catch(PDOException $e){
			$this->__logError($e->getMessage(),__FUNCTION__);
			throw new DatastoreException('Unable to login',2);
		}
	}
}