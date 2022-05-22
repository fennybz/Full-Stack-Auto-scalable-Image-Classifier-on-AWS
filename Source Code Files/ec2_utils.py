from secret_file import Access_key_ID , Secret_access_key
import boto3


def get_ec2_client():
    ec2 = boto3.client('ec2', region_name='us-east-1',
                    aws_access_key_id=Access_key_ID, 
                    aws_secret_access_key=Secret_access_key)
    return ec2

def create_new_instance(instance_name):
    """
    return:
        resp: Response of creating_new_instance
    """
    ec2 = get_ec2_client()
    resp = ec2.run_instances(
			TagSpecifications  = [
                             {
                                 'ResourceType':'instance',
                                 'Tags' : [
                                     {
                                         'Key':'Name',
                                         'Value':instance_name
                                     },
                                 ]
                             } 
                            ], 
                         ImageId = "ami-0a3586a30e074fd67" ,
                         MinCount = 1 , MaxCount = 1 , 
                         InstanceType = "t2.micro",
                         KeyName = "face_recognition_app_tier",
                         SecurityGroups = ["app-tier-security-group"]
                        )
    
    return resp


def terminate_instance(instance_id):
    """
    parameters: 
        instance_id: Instance Id of Ec2 instance to terminate.

    return:
        terminating_resp: Response of terminating ec2 instance 
    """
    ec2 = get_ec2_client()
    terminating_resp = ec2.terminate_instances(InstanceIds=[instance_id])
    return terminating_resp

