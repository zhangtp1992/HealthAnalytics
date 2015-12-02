<?php
class model{
	public $stats=['Dia','HDL','HR','LDL','Sys','Tri'];
	public $personData=[];
	public $minValue=0;
	public $maxValue=0;

	public function __construct($personData){
		$this->personData=$personData;
	}

	private function __branch($data){
		$m=count($data);
		for($i=0;$i<$m;$i++){
			$min=$data[$i]['Min'];
			$max=$data[$i]['Max'];
			$value=$data[$i]['value'];
			$attrib=$data[$i]['key'];
			$val_count=count($value);
			$matchValue=FALSE;
			$this->minValue=$min;
			$this->maxValue=$max;
			if($val_count==1){
				if($this->personData[$attrib]==$value[0]){$matchValue=TRUE;}
			}
			else{
				if($this->personData[$attrib]>=$value[0]&&$this->personData[$attrib]<=$value[1]){$matchValue=TRUE;}
			}
			if($matchValue){
				$this->__branch($data[$i]['children']);
				break;
			}
			//echo $value[0].'--'.$value[1].'**'.$min.'##'.$max.' '.$this->personData[$attrib].' '.$attrib."\r\n";
		}
	}

	public function getStats(){
		$results=[];
		foreach($this->stats as $key=>$val){
			$modelFile='model/'.$val.'_Models/'.$this->personData['State'].'_'.$val.'.json';
			$data=json_decode(file_get_contents($modelFile),TRUE);
			$this->__branch($data['children']);
			$results[$val]['min']=$this->minValue;
			$results[$val]['max']=$this->maxValue;
		}
		return $results;
	}
}