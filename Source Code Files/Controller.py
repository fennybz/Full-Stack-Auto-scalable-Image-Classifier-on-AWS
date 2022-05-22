from secret_file import Access_key_ID , Secret_access_key
import boto3
from Sqs_utils import get_queue_length
from ec2_utils import create_new_instance, terminate_instance


ec2 = boto3.resource('ec2', region_name='us-east-1',
                    aws_access_key_id=Access_key_ID, 
                    aws_secret_access_key=Secret_access_key)


worker_names = ['worker-1','worker-2','worker-3','worker-4','worker-5','worker-6','worker-7','worker-8','worker-9','worker-10','worker-11','worker-12','worker-13','worker-14', 'worker-15', 'worker-16', 'worker-17','worker-18','worker-19']
current_workers = set()

web_tier_instance = "i-0d316b2e9b7f0b888"

states = ["running" , "stopped" , "pending"]

running_instances = []
start_and_pending = 0
for instance in ec2.instances.all():
    if instance.id != web_tier_instance and instance.state['Name'] == "running" or instance.state['Name'] == "pending":
        try:
            current_workers.add(instance.tags[0]['Value'])
        except:
            pass
        start_and_pending +=1
	    
    if instance.id != web_tier_instance and instance.state['Name'] == "running":
            running_instances.append(instance.id)

available_names = [i  for i in worker_names if i not in current_workers]
        

length_of_queue = get_queue_length()
if length_of_queue == 0:
    #print("Here")
    if len(running_instances) > 0:
         terminate_instance(running_instances.pop())
    else:
        pass
else:
    ideal_number_of_instaces = min( max(1,length_of_queue// 4) , 19)
    if start_and_pending < ideal_number_of_instaces:
        start_instances = ideal_number_of_instaces - start_and_pending
        for i in range(start_instances):
            if len(available_names)> 0:
                    resp = create_new_instance(available_names.pop(0))
            else:
                    resp = create_new_instance("Some Worker")
    
    elif start_and_pending == ideal_number_of_instaces:
        pass
    
    else:
        if len(running_instances) > 0:
            terminate_instance(running_instances.pop())
        else:
            pass
