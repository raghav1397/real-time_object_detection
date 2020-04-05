scp /home/cern/.aws/credentials pi@192.168.0.28:/home/pi/.aws/
scp /home/cern/.aws/config pi@192.168.0.28:/home/pi/.aws/
scp uploader.py pi@192.168.0.28:/home/pi/Documents/Our_Codes/
scp pi_run.py pi@192.168.0.28:/home/pi/darknet/run.py
ssh-keyscan -H ec2-54-235-226-238.compute-1.amazonaws.com
scp -i "cc-proj.pem" /home/cern/.aws/credentials ubuntu@ec2-54-235-226-238.compute-1.amazonaws.com:/home/ubuntu/.aws/
scp -i "cc-proj.pem" /home/cern/.aws/config ubuntu@ec2-54-235-226-238.compute-1.amazonaws.com:/home/ubuntu/.aws/
scp -i "cc-proj.pem" new_controller.py ubuntu@ec2-54-235-226-238.compute-1.amazonaws.com:/home/ubuntu/controller.py
scp -i "cc-proj.pem" cc-proj.pem ubuntu@ec2-54-235-226-238.compute-1.amazonaws.com:/home/ubuntu/