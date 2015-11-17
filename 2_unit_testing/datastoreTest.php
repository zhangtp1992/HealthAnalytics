<?php include('datastore.php');
//include('C:\\Users\\Administrator\\Documents\\GitHub\\HealthAnalytics\\1_code\\Datastore\\datastore.php');



//$dir    = '';
//$files1 = scandir($dir);
//$files2 = scandir($dir, 1);

//print_r($files1);
//print_r($files2);



class DatastoreTest extends PHPUnit_Framework_TestCase
{
	public function setUp(){
		$this->ds=new datastore();
	}
	public function tearDown(){ }

    /**
     * @expectedException InvalidArgumentException
     */
    public function testException(){
    }
}