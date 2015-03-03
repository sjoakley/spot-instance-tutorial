from fabric.api import *
from fabric.contrib.files import append
from fabric.decorators import *

env.user = "ubuntu"

DOCKER_IMAGE_NAME = 'spot-tutorial-nginx'
DOCKER_CONTAINER_NAME = 'nginx'

def install_packages():
    '''
    Installs all necessary packages for the runtime environments.
    '''

    # Add the Oracle JDK repo.
    sudo('add-apt-repository -y ppa:webupd8team/java')

    # Add the docker repo.
    sudo('apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9')
    append('/etc/apt/sources.list.d/docker.list', 'deb https://get.docker.com/ubuntu docker main', use_sudo=True)

    sudo('apt-get update')

    # Add TLS support for apt.
    sudo('apt-get install -y apt-transport-https')

    # This silence the Oracle JDK license screen.
    sudo('echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections')

    sudo('apt-get install -y oracle-java7-installer')
    sudo('apt-get install -y oracle-java7-set-default')

    sudo('apt-get install -y build-essential')
    sudo('apt-get install -y libevent-dev')
    sudo('apt-get install -y python-dev')

    # Install python tools.
    sudo('apt-get install -y python-pip')
    sudo('pip install virtualenv')

    # Install Docker.
    sudo('apt-get install -y lxc-docker')

def setup_git_repository():
    '''
    Clones the git repository for the tutorial.
    '''
    # TODO: Checkout the git repository in the home directory.
    pass

def build_docker_image():
    '''
    Build the nginx docker container from the git repo.
    '''
    with cd('$HOME/spot-instance-tutorial/docker/nginx'):
        sudo('docker build -t %s .' % DOCKER_IMAGE_NAME)

def stop_docker_container():
    '''
    Stop the running nginx docker container.
    '''
    # TODO: Stop the docker container with the name DOCKER_CONTAINER_NAME if it is running.
    pass

def configure_webserver():
    '''
    Configure the webserver using docker.
    '''
    # Checkout the tutorial git repo and build the docker image.
    setup_git_repository()
    build_docker_image()

    # TODO: Start the docker container for the nginx server and have it listen on port 80.

@task
def setup_webserver():
    '''
    Entry task for installing and starting the webserver.
    '''
    install_packages()
    configure_webserver()

def setup_load_test_packages():
    '''
    Install the extra packages for Locust.
    '''
    setup_git_repository()

    with cd('$HOME/spot-instance-tutorial/'):
        run('./setup.sh')
        run('venv/bin/pip install -r locust/requirements.txt')

def start_load_test_master(target):
    '''
    Start the Locust master.
    '''
    with cd('$HOME/spot-instance-tutorial'):
        run('venv/bin/locust -f locust/locustfile.py -H %s --master' % target)

def start_load_test_slave(target, master):
    '''
    Start the Locust slave.
    '''
    with cd('$HOME/spot-instance-tutorial'):
        run('venv/bin/locust -f locust/locustfile.py -H %s --slave --master-host=%s' % (target, master))

@task
def setup_load_test_master(target):
    '''
    Setup and start the Locust master tester.
    '''
    install_packages()
    setup_load_test_packages()
    start_load_test_master(target)

@task
def setup_load_test_slave(target, master):
    '''
    Setup and start the Locust slave tester.
    '''
    install_packages()
    setup_load_test_packages()
    start_load_test_slave(target, master)
