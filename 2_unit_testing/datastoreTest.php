<?php include('datastore.php');
//include('C:\\Users\\Administrator\\Documents\\GitHub\\HealthAnalytics\\1_code\\Datastore\\datastore.php');


class DatastoreTest extends PHPUnit_Framework_TestCase
{
	protected static $ds;
	protected static $email='test@testemail.com';
	protected static $authtoken;

	public static function dataProvider(){
		return [[[
			'email'=>self::$email,
			'fname'=>'Test_fname',
			'lname'=>'Test_lname',
			'password'=>'123456'
		]]];
	}

	public static function setUpBeforeClass(){
		self::$ds=new datastore();
	}

	public static function tearDownAfterClass(){
		self::$ds->db->query('DELETE FROM people WHERE email="'.self::$email.'"');
		self::$ds->db->query('DELETE FROM session WHERE authtoken="'.self::$authtoken.'"');
		self::$ds=NULL;
	}

    /**
     * @param array $testData
	 * @dataProvider dataProvider
     */
	public function test_addUser(array $testData){
		$x=self::$ds->addUser($testData['fname'],$testData['lname'],$testData['email'],$testData['password']);
		$this->assertEquals('{"results":"User successfully created"}',$x);
	}

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the First Name
     */
    public function test_addUserMissingFnameException(){
    	self::$ds->addUser('','Smith','email@us.com','password');
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the Last Name
     */
    public function test_addUserMissingLnameException(){
    	self::$ds->addUser('Bob','','email@us.com','password');
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the E-Mail Address
     */
    public function test_addUserMissingEmailException(){
    	self::$ds->addUser('Bob','Smith','','password');
    }

    /**
     * @expectedException DatastoreException
	 * @expectedExceptionMessage You must provide the Password
     */
    public function test_addUserMissingPasswordException(){
    	self::$ds->addUser('Bob','Smith','email@us.com','');
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
	 * @expectedExceptionMessage You cannot retreive this user
     */
    public function test_getUserCannotRetreiveUserException(){
    	self::$ds->getUser('nobody@thisaddress.com',self::$authtoken);
	}
}