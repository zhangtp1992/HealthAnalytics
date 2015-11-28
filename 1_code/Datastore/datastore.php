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

	private function __authenticateUser($authtoken){
		try{
			$pstmt=$this->db->prepare('SELECT people.pkey,people.fname,people.lname,people.email FROM session INNER JOIN people ON people.pkey=session.person WHERE authtoken=?');
			$pstmt->execute([$authtoken]);
			if($pstmt->rowCount()>0){
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
				throw new DatastoreException('ERROR, Invalid password',3);
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

	public function getUser($email,$authtoken){
		$this->__authenticateUser($authtoken);
		try{
			$pstmt=$this->db->prepare('SELECT people.fname,people.lname,people.email FROM people WHERE email=?');
			$pstmt->execute([$email]);
			$rs=$pstmt->fetch(PDO::FETCH_ASSOC);
			if($rs['email']!=$this->authenticatedUser['email']){throw new DatastoreException('You cannot retrieve this user',2);}
			return json_encode($rs);
		}
		catch(PDOException $e){throw new DatastoreException('Unable to retrieve user',1);}
	}

	function addWorkout($authtoken,$workout_type,$distance,$workout_time,$calories){
		$this->__authenticateUser($authtoken);
		if(empty($workout_type)){throw new DatastoreException('You must provide the Workout Type',5);}
		if(empty($distance)){throw new DatastoreException('You must provide the Workout Distance',5);}
		if(empty($workout_time)){throw new DatastoreException('You must provide the Workout Time',5);}
		if(empty($calories)){throw new DatastoreException('You must provide the Workout Calories',5);}
		if(!is_numeric($distance)){throw new DatastoreException('Invalid Workout Distance',5);}
		if(!is_numeric($workout_time)){throw new DatastoreException('Invalid Workout Time',5);}
		if(!is_numeric($calories)){throw new DatastoreException('Invalid Workout Calories',5);}
		try{
			$pstmt=$this->db->prepare('INSERT INTO workout (workout_type,distance,workout_time,calories,person) VALUES (?,?,?,?,?)');
			$pstmt->execute([$workout_type,$distance,$workout_time,$calories,$this->authenticatedUser['pkey']]);
			return(json_encode(['workout_id'=>$this->db->lastInsertId()]));
		}
		catch(PDOException $e){throw new DatastoreException('Unable to save workout',1);}
	}

	function getAllWorkout($authtoken){
		$this->__authenticateUser($authtoken);
		try{
			$workout=[];
			$stmt=$this->db->query('SELECT workout.workout_id,workout_type,distance,workout_time,calories,ts,email FROM workout INNER JOIN people ON people.pkey=workout.`person`');
			if($stmt->rowCount()>0){
				while($rs=$stmt->fetch(PDO::FETCH_ASSOC)){
					$workout[]=$rs;
				}
			}
			return(json_encode($workout));
		}
		catch(PDOException $e){throw new DatastoreException('Unable to fetch all workouts',1);}
	}

	function getWorkout($authtoken,$workout_id){
		$this->__authenticateUser($authtoken);
		try{
			$pstmt=$this->db->prepare('SELECT workout.workout_id,workout_type,distance,workout_time,calories,ts,email FROM workout INNER JOIN people ON people.pkey=workout.`person` WHERE workout.workout_id=?');
			$pstmt->execute([$workout_id]);
			if($pstmt->rowCount()>0){
				$rs=$pstmt->fetch(PDO::FETCH_ASSOC);
				return(json_encode($rs));
			}
		}
		catch(PDOException $e){throw new DatastoreException('Unable to fetch workout',1);}
	}

}