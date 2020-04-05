# real-time_object_detection

How to run our code
1. First run cred_transfer.sh to transfer all the aws credentials and necessary scripts from local to raspberry pi and controller (ec2 instance). Note: Change the local directory in the script file before you run.
2. Run panda.py in raspberry pi inside the folder Darknet (This script runs a shell command which uses gnome terminal command to run recorder.py, uploader.py and pi_run.py in raspberry pi at the same time).
3. Make sure the static ec2 instance where the controller is present is running.

AWS Bucket Name:
Request Bucket - cc1-proj-req-bucket Response Bucket - cc1-proj-res-bucket

AWS Region:
us-east-1

AWS Credentials:
[default]
aws_access_key_id=ASIA3BVZ4SBEGPBBHJV3 aws_secret_access_key=KB42E2ZiGrsWF5IqvUuKgY AeGj7TCE7t/ogJohNE aws_session_token=FwoGZXIvYXdzEA8aDHgOtYIPQ/b+yP0piCK/AQpVjiQPHv6odiwwicB EqCashcOx74bt2pAy6VoqGJHmqPYrpInN9IaT8N7IgLvIKUITr8iZv3KuPa06AsWz4GfEnf4 WzOgD5DsoQVdDR9Ds21dAxF/VUZDoyHLT85qAs8fzdpmpcmrCb7TJL1sUM1J1geMF0J3 sSeqoBBH0b994bDCVVxfo3H+UJRpb1kFdTRtxY6GC6GY39MvAHaS/afi1BIAQNbQciPxqb ZO6bw/SUAvps7877LbxE1rDPwZAKJvZifQFMi20eBB3/uELMTW78zHuixJWniyPqG229pD kAxC5FuUHaw4rYNmRTBxVcAOrw1g=
