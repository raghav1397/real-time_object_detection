import time
import boto3
import urllib.request

EC2_RESOURCE = boto3.resource('ec2')
EC2_CLIENT = boto3.client('ec2')
SQS_RESOURCE = boto3.resource('sqs')
SQS_CLIENT = boto3.client('sqs')
PI_REQUESTS = 1
MAX_EC2_INSTANCES = 8
REQUEST_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/759525314632/cc-proj1-req-queue.fifo'
RESPONSE_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/759525314632/cc-proj1-res-queue.fifo'
free_instances_ids = []

def create_ec2_instances(number_of_instances=1):
    with open("/home/ubuntu/.aws/credentials", "r") as f:
        creds = f.read()
    with open("/home/ubuntu/.aws/config", "r") as f:
        config = f.read()
    script = '''#!/bin/bash
    mkdir /home/ubuntu/.aws
    echo "''' + creds + '''" > /home/ubuntu/.aws/credentials
    echo "''' + config + '''" > /home/ubuntu/.aws/config
    chown -R ubuntu: /home/ubuntu/.aws'''
    ins = EC2_RESOURCE.create_instances(
        ImageId='ami-09dc31fec649a466c',
        MinCount=1,
        MaxCount=number_of_instances,
        SecurityGroups=['launch-wizard-1'],
        InstanceType='t2.micro',
        KeyName='cc-proj',
        UserData=script
    )

def looper():
    
    global free_instances_ids
    flag = True
    controller_id = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read().decode().strip()
    
    while True:
        free_instances_ids = []
        instances = EC2_RESOURCE.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running','pending']}])
        for i in instances:
            if i.id != controller_id:
                free_instances_ids.append(i.id)
        
        number_of_requests = int(SQS_CLIENT.get_queue_attributes(QueueUrl=REQUEST_QUEUE_URL,
        AttributeNames=['ApproximateNumberOfMessages'])['Attributes']['ApproximateNumberOfMessages'])
        
        if number_of_requests > PI_REQUESTS:
            print("---------------------------------------------------------------------------------------------------------")
            print("Current # of Requests : {}".format(number_of_requests))
            # create new instances with a number set as min(20-len(self.), number_of_requests)
            number_of_instances_to_create = max(0,min(MAX_EC2_INSTANCES-len(free_instances_ids), number_of_requests-PI_REQUESTS-len(free_instances_ids)))
            if(number_of_instances_to_create > 0):
                print("Creating {} new instances".format(number_of_instances_to_create))
                create_ec2_instances(number_of_instances_to_create)
            flag = True

        else:
            if flag:
                print("Waiting")
                flag = False

if __name__ == "__main__":
    looper()