import os
import time
import boto3

if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))
    while True:
        if len(os.listdir(root+"/Recorded_Videos")) > 0:
            file_name = sorted(os.listdir(root+"/Recorded_Videos"))[0]
            time.sleep(1)
            print("Found file {}".format(file_name))
            # Upload file
            bucket_name = 'cc1-proj-req-bucket'
            s3_client = boto3.client('s3')
            print("Uploading file to S3")
            response = s3_client.upload_file(os.path.join(root+"/Recorded_Videos",file_name), bucket_name, file_name)
            print("Done uploading file to S3")
            # Push request
            sqs_client = boto3.client('sqs')
            queue = 'https://sqs.us-east-1.amazonaws.com/759525314632/cc-proj1-req-queue.fifo'
            print("Pushing reuest to queue")
            message = file_name
            response = sqs_client.send_message(
                QueueUrl=queue,
                MessageBody=message,
                MessageAttributes={
                    'Bucket_Name': {
                        'StringValue': bucket_name,
                        'DataType': 'String'
                    }
                },
                MessageGroupId='1')
            print("Done sending request")
            # Delete file
            os.remove(os.path.join(root+"/Recorded_Videos",file_name))
            print("File deleted")