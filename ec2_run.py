#!/bin/python3
import os
import time
import boto3
import urllib.request
from subprocess import call
from collections import Counter

class ObjectRecognition:

    def __init__(self):
        self.root = os.path.dirname(os.path.abspath(__file__)) + "/"
        self.SQS_CLIENT = boto3.client('sqs')
        self.S3_CLIENT = boto3.client('s3')
        self.S3_RESOURCE = boto3.resource('s3')
        self.REQUEST_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/759525314632/cc-proj1-req-queue.fifo'
        self.RESPONSE_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/759525314632/cc-proj1-res-queue.fifo'

    def download_from_s3(self):
        start = time.time()
        while True:
            resp = self.SQS_CLIENT.receive_message(
                QueueUrl=self.REQUEST_QUEUE_URL,
                MessageAttributeNames=['Bucket_Name'],
                MaxNumberOfMessages=1
            )
            if 'Messages' in resp.keys():
                break
            if time.time() - start > 60:
                return 'Fail'

        self.message = resp['Messages'][0]
        _ = self.SQS_CLIENT.delete_message(
               QueueUrl=self.REQUEST_QUEUE_URL,
               ReceiptHandle=self.message['ReceiptHandle']
            )
        self.file_name = self.message['Body']
        bucket_name = self.message['MessageAttributes']['Bucket_Name']['StringValue']
        
        print('Downloading ', self.file_name)
        self.S3_CLIENT.download_file(bucket_name, self.file_name, self.root+'video.h264')
        # If delete the input bucket files, uncomment these lines below
        # obj = self.S3_RESOURCE.Object(bucket_name,file_name)
        # obj.delete()
        return 'Success'

    def run_darknet(self):
        print('Running Darknet')
        code = os.system('Xvfb :1 & export DISPLAY=:1 ; ./darknet detector demo cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights video.h264 > result.txt')
        if code == 0:
            fp = open('result.txt', 'r')
            results, names = [], []
            lines = fp.read().splitlines()

            for line in lines:
                if '%' in line:
                    line = line.strip()
                    results.append([line.split(':')[0], line.split(':')[1]])
                    names.append(line.split(':')[0])
            fp.close()
            self.classes = list(Counter(names).keys())
            if len(self.classes) == 0:
                self.classes.append('Nothing')
            
            print('Found classes {}'.format(self.classes))
            
            with open(self.root+"classes.txt","w") as f:
                f.writelines("%s\t" % cls for cls in self.classes)
            self.upload_to_s3()
        else:
            response = self.SQS_CLIENT.send_message(
                QueueUrl=self.RESPONSE_QUEUE_URL,
                MessageBody=urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read().decode().strip() + " found {} error".format(self.file_name),
                MessageGroupId='1')
        
    def upload_to_s3(self):
        print('Uploading output')
        bucket_name = 'cc1-proj-res-bucket'
        response = self.S3_CLIENT.upload_file(self.root+"classes.txt", bucket_name, self.file_name)
        response = self.SQS_CLIENT.send_message(
                QueueUrl=self.RESPONSE_QUEUE_URL,
                MessageBody=urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read().decode().strip() + ' handled {}'.format(self.file_name),
                MessageGroupId='1')
        try:
            os.remove(self.root+"video.h264")
            os.remove(self.root+"result.txt")
            os.remove(self.root+"classes.txt")
        except:
            pass

if __name__ == '__main__':
    os.system("chmod u+x /home/pi/darknet/darknet")
    while True:
        tmp = ObjectRecognition()
        resp = tmp.download_from_s3()
        if resp == 'Fail':
            ec2 = boto3.resource('ec2')
            ec2.instances.filter(InstanceIds=[urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read().decode().strip()]).terminate()
        else:
            tmp.run_darknet()