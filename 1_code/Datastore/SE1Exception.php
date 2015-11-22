<?php
class SE1Exception extends Exception
{
    public function __construct($message, $code = 0) {
        parent::__construct($message,$code,null);
    }

    public function getHttpCode(){
    	switch($this->getCode()){
    		case 1:
    			return '404 Not Found';
    		break;
    		case 2:
    			return '500 Internal Service Error';
    		break;
    		case 3:
    			return '401 Unauthorized';
    		break;
    		case 4:
    			return '409 Conflict';
    		break;
    	}
    }
}