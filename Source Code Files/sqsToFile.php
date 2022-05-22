<?php
require '/var/www/html/vendor/autoload.php';

use Aws\Sqs\SqsClient;
use Aws\Exception\AwsException;

$start_time = time();
while ((time() - $start_time) < 600) {	
	$responseQueueUrl = 'https://sqs.us-east-1.amazonaws.com/670431221643/face-recogntion-response-queue';
	$sqsClient = new SqsClient([
        'credentials' => [
                'key'    => 'AKIAZYGGQS6F2Q7VYV7T',
                'secret' => '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',
            ],
            'region' => 'us-east-1',
            'version' => '2012-11-05'
        ]);
	$result = $sqsClient->receiveMessage(array(
                'AttributeNames' => ['SentTimestamp'],
                'MaxNumberOfMessages' => 10,
                'MessageAttributeNames' => ["ImageName"],
                'QueueUrl' => $responseQueueUrl,
                'WaitTimeSeconds' => 20,
	));
        if (!empty($result->get('Messages'))) {
		$i = 0;
                while($i < sizeof($result->get('Messages'))) {
			$message = $result->get('Messages')[$i];
			$imageName = $message['MessageAttributes']['ImageName']['StringValue'];
			$receiptHandle = $message['ReceiptHandle'];
			$classification = $message['Body']; 
			$filename = pathinfo($imageName, PATHINFO_FILENAME);
			$image_json_data  =json_encode([$classification, $receiptHandle]);
			file_put_contents("/var/www/html/classificationFolder/${filename}",$image_json_data, LOCK_EX);
			echo "${filename} written\n";
			$i++;
                }
	}
	sleep(5);
}

?>
