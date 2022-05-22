<?php
require 'vendor/autoload.php';
set_time_limit(0);
use Aws\Sqs\SqsClient;
use Aws\Exception\AwsException;

function sendImage($file, $name) {
    try {
        $requestQueueUrl = 'https://sqs.us-east-1.amazonaws.com/670431221643/face-recogntion-request-queue';
	$responseQueueUrl = 'https://sqs.us-east-1.amazonaws.com/670431221643/face-recogntion-response-queue';

        $sqsClient = new SqsClient([
        'credentials' => [
                'key'    => 'AKIAZYGGQS6F2Q7VYV7T',
                'secret' => '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',    
            ],
            'region' => 'us-east-1',
            'version' => '2012-11-05'
        ]);
        $imagelink = file_get_contents($file);
        $encdata = base64_encode($imagelink);    
	$sqsClient->sendMessage([
	    'MessageBody' => $encdata,
	    'QueueUrl' => $requestQueueUrl,
	    'MessageAttributes' => [
	        'ImageName' => [
		    'DataType' => "String",
		    'StringValue' => $name
		]
	    ]		
	]);
	$filename = pathinfo($name, PATHINFO_FILENAME);
	$start_time = time();
	#while(!is_readable("classificationFolder/${filename}" and (time() - $start_time) < 10)){
	while(!is_readable("classificationFolder/${filename}")) {
		if ((time() - $start_time) > 300) {
			break;
		}
		sleep(2);
	}
	$string = file_get_contents("classificationFolder/${filename}");
	$json_a = json_decode($string, true);
	$sqsClient->deleteMessage([
            'QueueUrl' => $responseQueueUrl, // REQUIRED
            'ReceiptHandle' => $json_a[1]
	]);
	unlink("classificationFolder/${filename}");
    	return $json_a[0];
    } catch (AwsException $e) {
        // output error message if fails
        error_log($e->getMessage());
    }
}
?>
