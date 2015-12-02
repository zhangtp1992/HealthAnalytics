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
			$pstmt=$this->db->prepare('SELECT people.pkey,people.fname,people.lname,people.email,people.role FROM session INNER JOIN people ON people.pkey=session.person WHERE authtoken=?');
			$pstmt->execute([$authtoken]);
			if($pstmt->rowCount()>0){
				$rs=$pstmt->fetch(PDO::FETCH_ASSOC);
				$this->authenticatedUser=$rs;
			}
			else{throw new DatastoreException('User is not authenticated',3);}
		}
		catch(PDOException $e){throw new DatastoreException('ERROR, unable to authenication user',2);}
	}

	#There is a bug with PHP PDO which causes non-strings to be cast as strings when pulled from the database
	private function __typecast($table,$record){
		$flds_int=[
			'workout'=>['workout_id','calories','duration'],
			'user'=>['waist_size','height','weight'],
			'food'=>['userfood_id','food','calories','serving_size_normalized']
		];
		foreach($flds_int[$table] as $key=>$val){
			if(isset($record[$val])){$record[$val]=(int)$record[$val];}
		}
		$flds_float=[
			'workout'=>['distance','pace'],
			'user'=>[],
			'food'=>['serving','total_calories','total_mass']
		];
		foreach($flds_float[$table] as $key=>$val){
			if(isset($record[$val])){$record[$val]=(float)$record[$val];}
		}

		return $record;
	}

	public function addFood($authtoken,$food,$serving,$meal,$food_timestamp,$comments){
		$this->__authenticateUser($authtoken);
		if(empty($food)){throw new DatastoreException('You must provide the Food',5);}
		if(empty($serving)){throw new DatastoreException('You must provide the Serving',5);}
		if(empty($meal)){throw new DatastoreException('You must provide the Meal',5);}
		if(empty($food_timestamp)){throw new DatastoreException('You must provide the Food Timestamp',5);}
		if(!is_numeric($serving)){throw new DatastoreException('Invalid Serving',5);}
		try{
			$pstmt=$this->db->prepare('INSERT INTO food (food,serving,meal,food_timestamp,comments,person) VALUES(?,?,?,?,?,?)');
			$pstmt->execute([$food,$serving,$meal,$food_timestamp,$comments,$this->authenticatedUser['pkey']]);
			return(json_encode(['userfood_id'=>$this->db->lastInsertId()]));
		}
		catch(PDOException $e){
			$this->__logError($e->getMessage(),__FUNCTION__);
			if($e->errorInfo[1]==1452){$txt='This food does not exist';$code=4;}
			else{$txt='Unable to create food';$code=2;}
			throw new DatastoreException($txt,$code);
		}
	}

	public function addUser($fname,$lname,$email,$passwd,$mi,$weight,$height,$birth_date,$gender,$waist_size,$address1,$address2,$city,$state,$zip){
		if(empty($fname)){throw new DatastoreException('You must provide the First Name',5);}
		if(empty($lname)){throw new DatastoreException('You must provide the Last Name',5);}
		if(empty($email)){throw new DatastoreException('You must provide the E-Mail Address',5);}
		if(empty($passwd)){throw new DatastoreException('You must provide the Password',5);}
		if(empty($mi)){throw new DatastoreException('You must provide the Middle Name Initial',5);}
		if(empty($weight)){throw new DatastoreException('You must provide the Weight',5);}
		if(empty($height)){throw new DatastoreException('You must provide the Height',5);}
		if(empty($birth_date)){throw new DatastoreException('You must provide the Birth Date',5);}
		if(empty($gender)){throw new DatastoreException('You must provide the Gender',5);}
		if(empty($waist_size)){throw new DatastoreException('You must provide the Waist Size',5);}
		if(empty($address1)){throw new DatastoreException('You must provide Address Line #1',5);}
		if(empty($city)){throw new DatastoreException('You must provide the City',5);}
		if(empty($state)){throw new DatastoreException('You must provide the State',5);}
		if(empty($zip)){throw new DatastoreException('You must provide the Zip Code',5);}
		if(!is_numeric($height)){throw new DatastoreException('Invalid Height',5);}
		if(!is_numeric($weight)){throw new DatastoreException('Invalid Weight',5);}
		if(!is_numeric($waist_size)){throw new DatastoreException('Invalid Waist Size',5);}
//$birth_date='2015-11-05T13:12:43.511Z';
//if (preg_match("/\d{4}-[0-1]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d:[0-5]\d\.?\d?\d?\d?Z/", $birth_date)) {
//    echo "A match was found.";
//} else {
//    echo "A match was not found.".$birth_date;
//}


		try{
			$pstmt=$this->db->prepare('INSERT INTO people (fname,lname,email,passwd,mi,weight,height,birth_date,gender,waist_size,address1,address2,city,state,zip) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)');
			$passwd=password_hash($passwd, PASSWORD_BCRYPT, ['cost'=>11]);
			$pstmt->execute([$fname,$lname,$email,$passwd,$mi,$weight,$height,$birth_date,strtoupper($gender),$waist_size,$address1,$address2,$city,$state,$zip]);
			return('{"results":"User successfully created"}');
		}
		catch(PDOException $e){
			$this->__logError($e->getMessage(),__FUNCTION__);
			if($e->errorInfo[1]==1062){$txt='This email address already exists';$code=4;}
			else{$txt='Unable to create user';$code=2;}
			throw new DatastoreException($txt,$code);
		}
	}

	function addWorkout($authtoken,$workout_type,$distance,$duration,$workout_timestamp,$calories,$comments){
		$this->__authenticateUser($authtoken);
		if(empty($workout_type)){throw new DatastoreException('You must provide the Workout Type',5);}
		if(empty($distance)){throw new DatastoreException('You must provide the Workout Distance',5);}
		if(empty($duration)){throw new DatastoreException('You must provide the Workout Duration',5);}
		if(empty($calories)){throw new DatastoreException('You must provide the Workout Calories',5);}
		if(empty($workout_timestamp)){throw new DatastoreException('You must provide the Workout Timestamp',5);}
		if(!is_numeric($distance)){throw new DatastoreException('Invalid Workout Distance',5);}
		if(!is_numeric($duration)){throw new DatastoreException('Invalid Workout Duration',5);}
		if(!is_numeric($calories)){throw new DatastoreException('Invalid Workout Calories',5);}
		try{
			$pstmt=$this->db->prepare('INSERT INTO workout (workout_type,distance,duration,calories,workout_timestamp,person,comments) VALUES (?,?,?,?,?,?,?)');
			$pstmt->execute([$workout_type,$distance,$duration,$calories,$workout_timestamp,$this->authenticatedUser['pkey'],$comments]);
			return(json_encode(['workout_id'=>$this->db->lastInsertId()]));
		}
		catch(PDOException $e){throw new DatastoreException('Unable to save workout',1);}
	}

	public function getUser($email,$authtoken){
		$this->__authenticateUser($authtoken);
		try{
			$pstmt=$this->db->prepare('SELECT fname,mi,lname,role,email,weight,height,birth_date,gender,waist_size,address1,address2,city,state,zip FROM people WHERE email=?');
			$pstmt->execute([$email]);
			$rs=$pstmt->fetch(PDO::FETCH_ASSOC);
			if($rs['email']!=$this->authenticatedUser['email']){throw new DatastoreException('You cannot retrieve this user',2);}
			return json_encode($this->__typecast('user',$rs));
		}
		catch(PDOException $e){throw new DatastoreException('Unable to retrieve user',1);}
	}

	function getFood($authtoken,$userfood_id){
		$this->__authenticateUser($authtoken);
		try{
			$valid=FALSE;
			$pstmt=$this->db->prepare('SELECT * FROM getFoodView WHERE userfood_id=?');
			$pstmt->execute([$userfood_id]);
			if($pstmt->rowCount()>0){
				$rs=$pstmt->fetch(PDO::FETCH_ASSOC);
				if($rs['email']==$this->authenticatedUser['email']){
					$valid=TRUE;
					return(json_encode($this->__typecast('food',$rs)));
				}
			}
			if(!$valid){throw new DatastoreException('Userfood_id not found',1);}
		}
		catch(PDOException $e){throw new DatastoreException('Unable to fetch food',2);}
	}

	function getFoodAll($authtoken){
		$this->__authenticateUser($authtoken);
		if($this->authenticatedUser['role']!='admin'){throw new DatastoreException('You do not have the rights to perform this action',3);}
		try{
			$food=[];
			$stmt=$this->db->query('SELECT * FROM getFoodView');
			if($stmt->rowCount()>0){
				while($rs=$stmt->fetch(PDO::FETCH_ASSOC)){
					$user[]=$this->__typecast('food',$rs);
				}
			}
			return(json_encode($user));
		}
		catch(PDOException $e){throw new DatastoreException('Unable to fetch all userfood',2);}
	}

	function getFoodList($authtoken){
		$this->__authenticateUser($authtoken);
		try{
			$food=[];
			$stmt=$this->db->query('SELECT * FROM food_list');
			if($stmt->rowCount()>0){
				while($rs=$stmt->fetch(PDO::FETCH_ASSOC)){
					$food[]=$this->__typecast('food',$rs);
				}
			}
			return(json_encode($food));
		}
		catch(PDOException $e){throw new DatastoreException('Unable to fetch food list',2);}
	}

	function getFoodUser($authtoken,$email){
		$this->__authenticateUser($authtoken);
		try{
			$valid=FALSE;
			if($email==$this->authenticatedUser['email']){
				$valid=TRUE;
				$pstmt=$this->db->prepare('SELECT * FROM getFoodView WHERE email=?');
				$pstmt->execute([$email]);
				if($pstmt->rowCount()>0){
					$food=[];
					while($rs=$pstmt->fetch(PDO::FETCH_ASSOC)){
						$food[]=$this->__typecast('food',$rs);
					}
				}
				else{$valid=FALSE;}
			}
			if(!$valid){throw new DatastoreException('User food not found',1);}
			else{return(json_encode($food));}
		}
		catch(PDOException $e){throw new DatastoreException('Unable to fetch user food',2);}
	}

	function getHealthStats($authtoken,$age,$height,$weight,$waist_size,$gender,$ethnicity,$state){
		include('health_stats.php');
		$person=['State'=>$state,'Gender'=>strtoupper($gender),'Waist'=>$waist,'Height'=>$height,'Age_years'=>$age,'Ethnicity'=>$ethnicity];
		$model=new model($person);
		return json_encode($model->getStats());
	}

	function getUserAll($authtoken){
		$this->__authenticateUser($authtoken);
		if($this->authenticatedUser['role']!='admin'){throw new DatastoreException('You do not have the rights to perform this action',3);}
		try{
			$user=[];
			$stmt=$this->db->query('SELECT fname,mi,lname,role,email,weight,height,birth_date,gender,waist_size,address1,address2,city,state,zip FROM people');
			if($stmt->rowCount()>0){
				while($rs=$stmt->fetch(PDO::FETCH_ASSOC)){
					$user[]=$this->__typecast('user',$rs);
				}
			}
			return(json_encode($user));
		}
		catch(PDOException $e){throw new DatastoreException('Unable to fetch all users',2);}
	}

	function getWorkout($authtoken,$workout_id){
		$this->__authenticateUser($authtoken);
		try{
			$valid=FALSE;
			$pstmt=$this->db->prepare('SELECT * FROM getWorkoutView WHERE workout_id=?');
			$pstmt->execute([$workout_id]);
			if($pstmt->rowCount()>0){
				$rs=$pstmt->fetch(PDO::FETCH_ASSOC);
				if($rs['email']==$this->authenticatedUser['email']){
					$valid=TRUE;
					return(json_encode($this->__typecast('user',$rs)));
				}
			}
			if(!$valid){throw new DatastoreException('Workout_id not found',1);}
		}
		catch(PDOException $e){throw new DatastoreException('Unable to fetch workout',2);}
	}

	function getWorkoutAll($authtoken){
		$this->__authenticateUser($authtoken);
		if($this->authenticatedUser['role']!='admin'){throw new DatastoreException('You do not have the rights to perform this action',3);}
		try{
			$workout=[];
			$stmt=$this->db->query('SELECT * FROM getWorkoutView');
			if($stmt->rowCount()>0){
				while($rs=$stmt->fetch(PDO::FETCH_ASSOC)){
					$workout[]=$this->__typecast('workout',$rs);
				}
			}
			return(json_encode($workout));
		}
		catch(PDOException $e){throw new DatastoreException('Unable to fetch food list',2);}
	}

	function getWorkoutUser($authtoken,$email){
		$this->__authenticateUser($authtoken);
		try{
			$valid=FALSE;
			if($email==$this->authenticatedUser['email']){
				$valid=TRUE;
				$pstmt=$this->db->prepare('SELECT * FROM getWorkoutView WHERE email=?');
				$pstmt->execute([$email]);
				if($pstmt->rowCount()>0){
					while($rs=$pstmt->fetch(PDO::FETCH_ASSOC)){
						$workout[]=$this->__typecast('workout',$rs);
					}
				}
				else{$valid=FALSE;}
			}
			if(!$valid){throw new DatastoreException('User workouts not found',1);}
			else{return(json_encode($workout));}
		}
		catch(PDOException $e){throw new DatastoreException('Unable to fetch user workouts',2);}
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

	public function logoutUser($authtoken,$user){
		$this->__authenticateUser($authtoken);
		try{
			if($user!=$this->authenticatedUser['email']){throw new DatastoreException('You cannot logout this user',2);}
			$pstmt=$this->db->prepare('DELETE FROM session WHERE person=? AND authtoken=?');
			$pstmt->execute([$this->authenticatedUser['pkey'],$authtoken]);
			return('{"results":"Logout Complete"}');
		}
		catch(PDOException $e){throw new DatastoreException('Unable to logout user',1);}
	}

	public function updateUser($fname,$lname,$email,$mi,$weight,$height,$birth_date,$gender,$waist_size,$address1,$address2,$city,$state,$zip,$authtoken){
		if(empty($fname)){throw new DatastoreException('You must provide the First Name',5);}
		if(empty($lname)){throw new DatastoreException('You must provide the Last Name',5);}
		if(empty($email)){throw new DatastoreException('You must provide the E-Mail Address',5);}
		if(empty($mi)){throw new DatastoreException('You must provide the Middle Name Initial',5);}
		if(empty($weight)){throw new DatastoreException('You must provide the Weight',5);}
		if(empty($height)){throw new DatastoreException('You must provide the Height',5);}
		if(empty($birth_date)){throw new DatastoreException('You must provide the Birth Date',5);}
		if(empty($gender)){throw new DatastoreException('You must provide the Gender',5);}
		if(empty($waist_size)){throw new DatastoreException('You must provide the Waist Size',5);}
		if(empty($address1)){throw new DatastoreException('You must provide Address Line #1',5);}
		if(empty($city)){throw new DatastoreException('You must provide the City',5);}
		if(empty($state)){throw new DatastoreException('You must provide the State',5);}
		if(empty($zip)){throw new DatastoreException('You must provide the Zip Code',5);}
		if(!is_numeric($height)){throw new DatastoreException('Invalid Height',5);}
		if(!is_numeric($weight)){throw new DatastoreException('Invalid Weight',5);}
		if(!is_numeric($waist_size)){throw new DatastoreException('Invalid Waist Size',5);}

		try{
			$this->__authenticateUser($authtoken);
			if($email!=$this->authenticatedUser['email']){throw new DatastoreException('You cannot update this user',2);}
			$pstmt=$this->db->prepare('UPDATE people SET fname=?,lname=?,mi=?,weight=?,height=?,birth_date=?,gender=?,waist_size=?,address1=?,address2=?,city=?,state=?,zip=? WHERE email=?');
			$pstmt->execute([$fname,$lname,$mi,$weight,$height,$birth_date,strtoupper($gender),$waist_size,$address1,$address2,$city,$state,$zip,$email]);
			return('{"results":"User successfully updated"}');
		}
		catch(PDOException $e){
			$this->__logError($e->getMessage(),__FUNCTION__);
			throw new DatastoreException('Unable to create user',2);
		}
	}
}