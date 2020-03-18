<?php

$startTime = microtime(true);
$initialMemory = memory_get_usage();
$runningTime =  microtime(true) - $startTime;
$usedMemory = (memory_get_peak_usage() - $initialMemory) / (1024 * 1024);
var_dump('running time: ' . $runningTime . ' [s]');
var_dump('used memory: ' . $usedMemory . ' [MB]');

?>