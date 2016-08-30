#!/usr/bin/env python

import os
import sys
import boto3
import argparse

global pars

pars = argparse.ArgumentParser (description="AWS Autoscaling Parser", epilog="Thanks for using!", prog="AWS Autoscaling parser")
pars.add_argument('-a', '--access', help="The access key for your AWS account.")
pars.add_argument('-s', '--secret', help="The secret key for your AWS account.")
pars.add_argument('-r', '--region', help="AWS region.")

arg = vars(pars.parse_args())

if len(sys.argv) < 3:
    if not os.path.isfile(os.path.expanduser("~/.aws/credentials")):
        print ('Can not detect AWS configuration file. Please, use "aws configure" or "--help"')
        pars.print_help()
        sys.exit(1)
    else:
        as_client = boto3.client(
        'autoscaling',
        )
        ec2_client = boto3.client(
        'ec2',
        )       
else:
    AWS_ACCESS_KEY_ID=arg['access']
    AWS_SECRET_ACCESS_KEY=arg['secret']
    os.environ ["AWS_DEFAULT_REGION"] = arg['region']
    as_client = boto3.client(
    'autoscaling',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def as_group():
        autoscalegroups = []
        for asg in as_client.describe_auto_scaling_groups().get('AutoScalingGroups'):
                asgname = asg.get('AutoScalingGroupName')
                autoscalegroups.append(asgname)
        return autoscalegroups

def as_ec2(asgroup):
    ec2_list = []
    instance_meta = as_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asgroup]).get('AutoScalingGroups')[0].get('Instances')
    for node in instance_meta:
            ec2_id = node.get('InstanceId')
            ec2_list.append(ec2_id)
    return ec2_list

def ec2_lifecycle(ec2):
    life_state = as_client.describe_auto_scaling_instances(InstanceIds=[ec2]).get('AutoScalingInstances')[0].get('LifecycleState')
    print "{0}\t\t".format(life_state),

def ec2_health(ec2):
    ec2_health = as_client.describe_auto_scaling_instances(InstanceIds=[ec2]).get('AutoScalingInstances')[0].get('HealthStatus')
    print "{0}\t\t".format(ec2_health),

def ec2_ip(ec2):
    private_ip = ec2_client.describe_instances(DryRun=False, InstanceIds=[ec2]).get('Reservations')[0].get('Instances')[0].get('PrivateIpAddress')
    public_ip = ec2_client.describe_instances(DryRun=False, InstanceIds=[ec2]).get('Reservations')[0].get('Instances')[0].get('PublicIpAddress')
    print "{0}\t\t".format(private_ip),
    print "{0}\t\t".format(public_ip),

def ec2_protection(ec2):
    ec2_prot_state = as_client.describe_auto_scaling_instances(InstanceIds=[ec2]).get('AutoScalingInstances')[0].get('ProtectedFromScaleIn')
    print "{0}\t\t".format(ec2_prot_state),

if __name__ == "__main__" :


    print ('Auto Scaling')
    print ('============')
    print ('Scaling-Group' + '\t\t\t' + 'Instances' + '\t\t' + 'Lifecycle' + '\t\t' + 'Health' + '\t\t' + 'Protection' + '\t\t' + 'PrivateIP' + '\t\t' + 'PublicIP')
    print ('-------------' + '\t\t\t' + '---------' + '\t\t' + '---------' + '\t\t' + '------' + '\t\t' + '----------' + '\t\t' + '---------' + '\t\t' + '--------')
    for group in as_group():
        print "{0:30}\t\t".format(group).ljust(30),
        i = 0
        for ec2 in as_ec2(group):
            if (i != 0):
                print "\t\t\t\t",
            print "{0}\t\t".format(ec2),
            ec2_lifecycle(ec2)
            ec2_health(ec2)
            ec2_protection(ec2)
            ec2_ip(ec2)
            i = i+1
            print "\n"
