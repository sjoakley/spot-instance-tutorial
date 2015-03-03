#!/usr/bin/env python

import argparse
import boto.ec2
from fabfile import *
from fabric.api import env, execute

parser = argparse.ArgumentParser(description='Query and configure EC2 spot instances.')
parser.add_argument('-r', '--region', default='us-east-1', help='EC2 region for cluster.')
parser.add_argument('-i', '--keyfile', required=True, help='Path to the keyfile to use with the cluster.')

def setup_fabric_env(keyfile):
    env.parallel = True
    env.key_filename = keyfile
    # NOTE(soakley): In general this is a very bad idea! However, since the purpose of this script is to setup and
    # teardown clusters it is reasonable to assume that the host keys will not match when recreating a cluster with
    # the same name as a previous cluster.
    env.disable_known_hosts = True

    #TODO: Set this to the list of host that you want to run fabric commands on.
    env.hosts = []

    # TODO: Use this to assign roles to hosts to leverage the @role decorator in fabric configure the set of
    # tasks that are run on each host.
    env.roledefs = {}

def main():
    args = parser.parse_args()

    self.ec2_conn = boto.ec2.connect_to_region(args.region)

    # TODO: Query the EC2 instances that were launched by the spot reuqests.
    # See http://boto.readthedocs.org/en/latest/ec2_tut.html
    # and http://boto.readthedocs.org/en/latest/ref/ec2.html for more details.


    # TODO: Use the execute command to run fabric tasks from this script.
    # See http://docs.fabfile.org/en/latest/usage/execution.html for more details.
    # execute(<task_name>, args)


if __name__ == "__main__":
    main()
