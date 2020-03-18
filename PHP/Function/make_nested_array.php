<?php

$input = "i/have/a/pen";
$array = explode( '/', $input );
//ネストした連想配列を作成
foreach( array_reverse($array) as $key ) {
    $tmpArr = [$key => $tmpArr];

}
print_r($tmpArr);
//空だったり、配列以外の値を持っていたりすると困るので前処理
if( !is_array($hoge) ) $hoge = [];
$hoge = array_merge_recursive($hoge, $tmpArr);
print_r($hoge);

?>
