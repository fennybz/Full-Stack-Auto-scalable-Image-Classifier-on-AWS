from secret_file import Access_key_ID , Secret_access_key
import boto3
from recognize_face import get_face
import base64
import time
from Sqs_utils import send_message, get_message , delete_recent, get_queue_length 

def upload_to_s3(image , image_name , prediction):
    s3 = boto3.client('s3',region_name='us-east-1',
                    aws_access_key_id=Access_key_ID, 
                    aws_secret_access_key=Secret_access_key)
    try:
        prediction_name = image_name[:-4] + " : " + prediction
        s3.upload_file(image , "face-recognition-s3-img" ,image_name)
        s3.upload_file(image , "face-recognition-s3-name" ,prediction_name) 
    except:
        print("Error while uploading")

def generate_image(msg):
    decoded_string = base64.b64decode(msg)
    filename = 'some_image.jpg'  
    with open(filename, 'wb') as f:
        f.write(decoded_string)
    f.close()

if __name__ == "__main__":
    while(True):
        queue_length = get_queue_length()
        print(str(queue_length))
        if queue_length > 0:
            msg , receipt_handle , image_name = get_message()
            if (msg != None and receipt_handle != None and image_name != None):
                generate_image(msg)
                prediction = get_face("some_image.jpg")
                upload_to_s3("some_image.jpg" , image_name , prediction)
                send_message(prediction, image_name)
                delete_recent(receipt_handle)
                
                time.sleep(1)
        else:
            time.sleep(1)
            
        
    



