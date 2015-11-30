<?php include('datastore.php');
//include('C:\\Users\\Administrator\\Documents\\GitHub\\HealthAnalytics\\1_code\\Datastore\\datastore.php');


class DatastoreTest extends PHPUnit_Framework_TestCase
{
	protected static $ds;
	protected static $email='test@testemail.com';
	protected static $authtoken;
	protected static $workout_id;

	public static function dataProvider(){
		return [[[
			'email'=>self::$email,
			'password'=>'123456'
		]]];
	}

	public static function setUpBeforeClass(){
		self::$ds=new datastore();
	}

	public static function tearDownAfterClass(){
		self::$ds->db->query('DELETE FROM people WHERE email="'.self::$email.'"');
		self::$ds->db->query('DELETE FROM session WHERE authtoken="'.self::$authtoken.'"');
		//self::$ds->db->query('DELETE FROM workout WHERE workout_id="'.self::$workout_id.'"');
		self::$ds=NULL;
	}

    /**
     * @param array $testData
	 * @dataProvider dataProvider
     */
	public function test_addUser(array $testData){
		$x=self::$ds->addUser('Bob','Smith',$testData['email'],$testData['password'],'E',220,72,'1987-09-16T00:00:00Z','M',34,'123 Easy Street','A2','Edison','NJ','08854');
		$this->assertEquals('{"results":"User successfully created"}',$x);
	}

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the First Name
     */
    public function test_addUserMissingFnameException(){
    	self::$ds->addUser('','Smith','email@us.com','password','E',220,72,'1987-09-16T00:00:00Z','M',34,'123 Easy Street','A2','Edison','NJ','08854');
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the Last Name
     */
    public function test_addUserMissingLnameException(){
    	self::$ds->addUser('Bob','','email@us.com','password','E',220,72,'1987-09-16T00:00:00Z','M',34,'123 Easy Street','A2','Edison','NJ','08854');
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the E-Mail Address
     */
    public function test_addUserMissingEmailException(){
    	self::$ds->addUser('Bob','Smith','','password','E',220,72,'1987-09-16T00:00:00Z','M',34,'123 Easy Street','A2','Edison','NJ','08854');
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the Password
     */
    public function test_addUserMissingPasswordException(){
    	self::$ds->addUser('Bob','Smith','email@us.com','','E',220,72,'1987-09-16T00:00:00Z','M',34,'123 Easy Street','A2','Edison','NJ','08854');
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the Middle Name Initial
     */
    public function test_addUserMissingMiddleNameInitialException(){
    	self::$ds->addUser('Bob','Smith','email@us.com','password','',220,72,'1987-09-16T00:00:00Z','M',34,'123 Easy Street','A2','Edison','NJ','08854');
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the Weight
     */
    public function test_addUserMissingWeightException(){
    	self::$ds->addUser('Bob','Smith','email@us.com','password','E','',72,'1987-09-16T00:00:00Z','M',34,'123 Easy Street','A2','Edison','NJ','08854');
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the Height
     */
    public function test_addUserMissingHeightException(){
    	self::$ds->addUser('Bob','Smith','email@us.com','password','E',220,'','1987-09-16T00:00:00Z','M',34,'123 Easy Street','A2','Edison','NJ','08854');
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the Birth Date
     */
    public function test_addUserMissingBirthDateException(){
    	self::$ds->addUser('Bob','Smith','email@us.com','password','E',220,72,'','M',34,'123 Easy Street','A2','Edison','NJ','08854');
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the Gender
     */
    public function test_addUserMissingGenderException(){
    	self::$ds->addUser('Bob','Smith','email@us.com','password','E',220,72,'1987-09-16T00:00:00Z','',34,'123 Easy Street','A2','Edison','NJ','08854');
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the Waist Size
     */
    public function test_addUserMissingWaistSizeException(){
    	self::$ds->addUser('Bob','Smith','email@us.com','password','E',220,72,'1987-09-16T00:00:00Z','M','','123 Easy Street','A2','Edison','NJ','08854');
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide Address Line #1
     */
    public function test_addUserMissingAddressLine1Exception(){
    	self::$ds->addUser('Bob','Smith','email@us.com','password','E',220,72,'1987-09-16T00:00:00Z','M',34,'','A2','Edison','NJ','08854');
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the City
     */
    public function test_addUserMissingCityException(){
    	self::$ds->addUser('Bob','Smith','email@us.com','password','E',220,72,'1987-09-16T00:00:00Z','M',34,'123 Easy Street','A2','','NJ','08854');
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the State
     */
    public function test_addUserMissingStateException(){
    	self::$ds->addUser('Bob','Smith','email@us.com','password','E',220,72,'1987-09-16T00:00:00Z','M',34,'123 Easy Street','A2','Edison','','08854');
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the Zip Code
     */
    public function test_addUserMissingZipCodeException(){
   	 	self::$ds->addUser('Bob','Smith','email@us.com','password','E',220,72,'1987-09-16T00:00:00Z','M',34,'123 Easy Street','A2','Edison','NJ','');
   	}

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage Invalid Height
     */
    public function test_addUserInvalidHeightException(){
   	 	self::$ds->addUser('Bob','Smith','email@us.com','password','E',220,'72x','1987-09-16T00:00:00Z','M',34,'123 Easy Street','A2','Edison','NJ','08854');
   	}
    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage Invalid Weight
     */
    public function test_addUserInvalidWeightException(){
   	 	self::$ds->addUser('Bob','Smith','email@us.com','password','E','2sd',72,'1987-09-16T00:00:00Z','M',34,'123 Easy Street','A2','Edison','NJ','08854');
   	}
    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage Invalid Waist Size
     */
    public function test_addUserInvalidWaistSizeException(){
   	 	self::$ds->addUser('Bob','Smith','email@us.com','password','E',220,72,'1987-09-16T00:00:00Z','M','sd34f-','123 Easy Street','A2','Edison','NJ','08854');
   	}

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage ERROR, Invalid password
     * @param array $testData
	 * @dataProvider dataProvider
     */
    public function test_loginUserIncorrectPasswordException(array $testData){
    	self::$ds->loginUser($testData['email'],'65984');
	}

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage E-Mail Address not found
     * @param array $testData
	 * @dataProvider dataProvider
     */
    public function test_loginUserEmailAddressNotFoundException(array $testData){
    	self::$ds->loginUser('nobody@thisaddress.com',$testData['password']);
	}

    /**
     * @param array $testData
	 * @dataProvider dataProvider
     */
    public function test_loginUserCorrectPassword(array $testData){
    	$x=self::$ds->loginUser($testData['email'],$testData['password']);
    	$token=json_decode($x,TRUE);
    	self::$authtoken=$token['authtoken'];
    	$this->assertRegExp('/{"authtoken":"/', $x);
	}

    /**
     * @param array $testData
	 * @dataProvider dataProvider
     */
	public function test_successfulGetUser(array $testData){
		$x=self::$ds->getUser($testData['email'],self::$authtoken);
		$this->assertRegExp('/{"fname":"/', $x);
	}

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You cannot retrieve this user
     */
    public function test_getUserCannotRetreiveUserException(){
    	self::$ds->getUser('nobody@thisaddress.com',self::$authtoken);
	}

	public function test_addWorkout(){
		$x=self::$ds->addWorkout(self::$authtoken,'run',1.00,120.0,0.5,'2015-11-05T13:12:43.511Z',200.00);
		$newWorkout=json_decode($x,TRUE);
		self::$workout_id=$newWorkout['workout_id'];
		$this->assertRegExp('/{"workout_id":"/', $x);
	}

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the Workout Type
     */

    public function test_addWorkoutMissingWorkoutTypeException(){
    	$x=self::$ds->addWorkout(self::$authtoken,'',1.00,120.0,0.5,'2015-11-05T13:12:43.511Z',200.00);
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the Workout Distance
     */

    public function test_addWorkoutMissingWorkoutDistanceException(){
    	$x=self::$ds->addWorkout(self::$authtoken,'run','',120.0,0.5,'2015-11-05T13:12:43.511Z',200.00);
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the Workout Duration
     */
    public function test_addWorkoutMissingWorkoutDurationException(){
    	$x=self::$ds->addWorkout(self::$authtoken,'run',1.00,'',0.5,'2015-11-05T13:12:43.511Z',200.00);
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the Workout Pace
     */
    public function test_addWorkoutMissingWorkoutPaceException(){
    	$x=self::$ds->addWorkout(self::$authtoken,'run',1.00,120.0,'','2015-11-05T13:12:43.511Z',200.00);
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the Workout Timestamp
     */
    public function test_addWorkoutMissingWorkoutTimestampException(){
    	$x=self::$ds->addWorkout(self::$authtoken,'run',1.00,120.0,0.5,'',200.00);
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the Workout Calories
     */
    public function test_addWorkoutMissingWorkoutCaloriesException(){
    	$x=self::$ds->addWorkout(self::$authtoken,'run',1.00,120.0,0.5,'2015-11-05T13:12:43.511Z','');
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage Invalid Workout Distance
     */
    public function test_addWorkoutInvalidWorkoutDistanceException(){
    	$x=self::$ds->addWorkout(self::$authtoken,'run','1.00x',120.0,0.5,'2015-11-05T13:12:43.511Z',200.00);
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage Invalid Workout Duration
     */
    public function test_addWorkoutInvalidWorkoutDurationException(){
    	$x=self::$ds->addWorkout(self::$authtoken,'run',1.00,'120.0ddd',0.5,'2015-11-05T13:12:43.511Z',200.00);    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage Invalid Workout Calories
     */
    public function test_addWorkoutInvalidWorkoutCaloriesException(){
    	    	$x=self::$ds->addWorkout(self::$authtoken,'run',1.00,120.0,0.5,'2015-11-05T13:12:43.511Z','20.dfer');
    }
}