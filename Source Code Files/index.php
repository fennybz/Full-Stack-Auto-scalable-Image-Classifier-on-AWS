<?php
use Aws\Sqs\SqsClient;
use Aws\Exception\AwsException;
set_time_limit(0);
$upload_dir = 'upload_images';
require __DIR__ . '/imageToSqs.php';
// "myfile" is the key of the http payload
$name = basename($_FILES["myfile"]["name"]);
$target_file = "$upload_dir/$name";
if (!move_uploaded_file($_FILES["myfile"]["tmp_name"], $target_file))
    echo 'error: '.$_FILES["myfile"]["error"].' see /var/log/apache2/error.log for details.';
else
    echo sendImage($target_file, $name);
?>
