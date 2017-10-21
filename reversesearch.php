// signing in and verifying

<?php
$data = array("uid"=>7286,"expires"=>1508561461,"auth"=>"73edd0303dc431d5ab8b9dcc4a380d85");
$json = json_encode($data);
$context = stream_context_create(array(
 'http' => array(
   "method" => "POST",
   "Content-Type: application/json\r\n",
   'content' => $json
 	)
 );
$response = file_get_contents($endpoint, FALSE, $context);

$uid = 7286;
$apikey = "b601cddd5a9e0506629782d3bd2869ea";
$expires = time() + 300; //

"auth":"34ec82c51d90f3227a70a105e477960a"

$uid = 1;
$apikey = "";
$expires = time()+300; // Expires - when the signature will become invalid (UNIX timestamp) - may be no more than 1200 seconds from now.

// Generate auth
$stringToHash = $uid."-".$expires."-".$apikey;
$auth = md5($stringToHash);

$data = array("uid"=>$uid,"expires"=>$expires,"auth"=>$auth);
?>

// Check images using Incandescent API_key

<?php
// assumes there is only one image in the directory with a .jpg extension
$directory = "/Documents/MVP/images";

// $images = array("http://www.domain.com/images/1.jpg","http://www.domain.com/images/2.jpg");
$images = glob($directory , "*.jpg"); // returns an array

$data = array("uid"=>$uid,"expires"=>$expires,"auth"=>$auth,"images"=>$images,"multiple"=>5);
$json = json_encode($data);
$context = stream_context_create(array(
		'http' => array(
			'method' => 'POST',
			"Content-Type: application/json\r\n",
			'content' => $json
		)
	));
$response = file_get_contents("https://incandescent.xyz/api/add/", FALSE, $context);
?>

// have to wait at least 5 seconds before calling this

<?php

$data = array("uid"=>$uid,"expires"=>$expires,"auth"=>$auth,"project_id"=>$project_id);
$json = json_encode($data);
$context = stream_context_create(array(
		'http' => array(
			'method' => 'POST',
			"Content-Type: application/json\r\n",
			'content' => $json
		)
	));
$response = file_get_contents("https://incandescent.xyz/api/get/", FALSE, $context);
?>
