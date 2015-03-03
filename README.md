# spot-instance-tutorial

## Setup
1. Clone the repository 'git clone https://github.com/sjoakley/spot-instance-tutorial.git'
2. Run the setup script './setup.sh'
3. Follow the steps outlined in the following link to create an EC2 keypair.
http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#having-ec2-create-your-key-pair

## The Task
The goal of this project is familiarize you with EC2 spot instances and a few
tools to make them easier to work with. To that end, we will leverage spot
instances to run a fleet of web servers and run a distributed load test. For
load testing we will use Locust.io (http://locust.io/) to run distributed
load generation.

At the end of the exercise you will have one webserver running Nginx serving a
static page, one machine for the Locust master and several instances for locust
slaves.

To setup the environment once the exercise steps are complete run the following
sequence of commands:

- Launch the spot instances './cli/launch.sh <keypair-name>'
- Wait for the spot instances to be launched, and choose roles for the hosts. You will need the following roles.
    - webserver: This will be the instance that runs Nginx.
    - locust_master: This will run the Locust load test master.
    - locust_slave: This will be a list of one or more instances that will be Locust slaves.
- Setup the webserver
```
fab -f fabric/fabfile.py -i <ec2_keyfile> -H <webserver> setup_webserver
```
- Configure the Locust master.
```
fab -f fabric/fabfile.py -i <ec2_keyfile> -H <locust_master> setup_load_test_master:target=http://<webserver>
```
- Start the Locust slaves.
```
fab -f fabric/fabfile.py -i <ec2_keyfile> -H [locust_slave,...] setup_load_test_slave:target=http://<webserver>,master=<locust_master>
```
- Visit the page http://<webserver>:8089 and start a load test. Repeat test with varying numbers of users until requests begin to fail.

### Steps
- Modify the file cli/launch.py to create additional instances for the load generators.
    - Bonus points for using different size hosts for the Locust master and slaves.
- Complete the TODO sections in fabric/fabfile.py.
    - Implement the setup\_git\_repository method to clone the git repo for the tutorial.
    - Implement the stop\_docker\_container method to stop any running Docker containers that may be previous runs of the fabric file.
    - Complete the configure\_webserver method stop previous containers and launch a new one from the freshly built image.

At this point you will be able to run steps 1 through 6 outlined above. However,
this approach requires waiting for the instance to launch and manually
executing the subsequent commands. We can take this a step further by
leveraging Boto to wait for the instances to become ready, and then
programmatically run fabric. So your final task is as follows:

![Alt text](http://www.online-image-editor.com//styles/2014/images/example_image.png "Optional title")

- Complete the fabric/wrapper.py script to automate steps 2 through 4 in the steps above.

## The Solution
You can find a reference implementation to this exercise in the 'solution'
branch.
