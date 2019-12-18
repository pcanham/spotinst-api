#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import boto3
import botocore.exceptions
import time
import sys
import os
import argparse
import random
import string
import logger


StartTime = time.time()
log = logger.logging.getLogger(__name__)

def randomStringwithDigits(stringLength=10):
    """Generate a random string of letters, digits and special characters """

    password_characters = string.ascii_letters + string.digits
    return ''.join(random.choice(password_characters) for i in range(stringLength))


# Create a policy
my_managed_policy = {
  'Version': '2012-10-17',
  'Statement': [
    {
      'Sid': 'GeneralSpotInstancesAccess',
      'Action': [
        'ec2:RequestSpotInstances',
        'ec2:CancelSpotInstanceRequests',
        'ec2:CreateSpotDatafeedSubscription',
        'ec2:Describe*',
        'ec2:AssociateAddress',
        'ec2:AttachVolume',
        'ec2:ConfirmProductInstance',
        'ec2:CopyImage',
        'ec2:CopySnapshot',
        'ec2:CreateImage',
        'ec2:CreateSnapshot',
        'ec2:CreateTags',
        'ec2:CreateVolume',
        'ec2:DeleteTags',
        'ec2:DisassociateAddress',
        'ec2:ModifyImageAttribute',
        'ec2:ModifyInstanceAttribute',
        'ec2:MonitorInstances',
        'ec2:RebootInstances',
        'ec2:RegisterImage',
        'ec2:RunInstances',
        'ec2:StartInstances',
        'ec2:StopInstances',
        'ec2:TerminateInstances',
        'ec2:UnassignPrivateIpAddresses',
        'ec2:DeregisterImage',
        'ec2:DeleteSnapshot',
        'ec2:DeleteVolume',
        'ec2:ModifyReservedInstances',
        'ec2:CreateReservedInstancesListing',
        'ec2:CancelReservedInstancesListing',
        'ec2:ModifyNetworkInterfaceAttribute',
        'ec2:DeleteNetworkInterface'
      ],
      'Effect': 'Allow',
      'Resource': [
        '*'
      ]
    },
    {
      'Sid': 'AccessELB',
      'Action': [
        'elasticloadbalancing:Describe*',
        'elasticloadbalancing:Deregister*',
        'elasticloadbalancing:Register*',
        'elasticloadbalancing:RemoveTags',
        'elasticloadbalancing:RegisterTargets',
        'elasticloadbalancing:EnableAvailabilityZonesForLoadBalancer',
        'elasticloadbalancing:DisableAvailabilityZonesForLoadBalancer'
      ],
      'Effect': 'Allow',
      'Resource': [
        '*'
      ]
    },
    {
      'Sid': 'AccessCloudWatch',
      'Action': [
        'cloudwatch:DescribeAlarmHistory',
        'cloudwatch:DescribeAlarms',
        'cloudwatch:DescribeAlarmsForMetric',
        'cloudwatch:GetMetricStatistics',
        'cloudwatch:ListMetrics',
        'cloudwatch:PutMetricData',
        'cloudwatch:PutMetricAlarm'
      ],
      'Effect': 'Allow',
      'Resource': [
        '*'
      ]
    },
    {
      'Sid': 'AccessSNS',
      'Action': [
        'sns:Publish',
        'sns:ListTopics',
        'sns:CreateTopic',
        'sns:GetTopicAttributes',
        'sns:ListSubscriptionsByTopic',
        'sns:Subscribe'
      ],
      'Effect': 'Allow',
      'Resource': [
        '*'
      ]
    },
    {
      'Sid': 'AccessIAM',
      'Action': [
        'iam:AddRoleToInstanceProfile',
        'iam:ListInstanceProfiles',
        'iam:ListInstanceProfilesForRole',
        'iam:PassRole',
        'iam:ListRoles',
        'iam:ListAccountAliases',
        'iam:GetPolicyVersion',
        'iam:ListPolicies',
        'iam:GetPolicy',
        'iam:ListAttachedRolePolicies',
        'organizations:ListAccounts',
        'iam:CreateServiceLinkedRole',
        'iam:PutRolePolicy',
        'iam:GetInstanceProfile',
        'iam:GetRolePolicy',
        'iam:ListRolePolicies'
      ],
      'Effect': 'Allow',
      'Resource': [
        '*'
      ]
    },
    {
      'Sid': 'GeneralAccessElaticBeanstalk',
      'Action': [
        'elasticbeanstalk:Describe*',
        'elasticbeanstalk:RequestEnvironmentInfo',
        'elasticbeanstalk:RetrieveEnvironmentInfo',
        'elasticbeanstalk:ValidateConfigurationSettings',
        'elasticbeanstalk:UpdateEnvironment',
        'elasticbeanstalk:ListPlatformVersions',
        'cloudformation:GetTemplate',
        'cloudformation:DescribeStackResources',
        'cloudformation:DescribeStackResource',
        'cloudformation:DescribeStacks',
        'cloudformation:ListStackResources',
        'cloudformation:UpdateStack',
        'cloudformation:DescribeStackEvents',
        'logs:PutRetentionPolicy',
        'logs:createLogGroup'
      ],
      'Effect': 'Allow',
      'Resource': [
        '*'
      ]
    },
    {
      'Sid': 'AccessAutoScalingGroups',
      'Action': [
        'autoscaling:*'
      ],
      'Effect': 'Allow',
      'Resource': [
        '*'
      ]
    },
    {
      'Sid': 'AccessEks',
      'Action': [
        'eks:ListClusters'
      ],
      'Effect': 'Allow',
      'Resource': [
        '*'
      ]
    },
    {
      'Sid': 'AccessEMR',
      'Action': [
        'elasticmapreduce:*',
        's3:GetObject'
      ],
      'Effect': 'Allow',
      'Resource': [
        '*'
      ]
    },
    {
      'Sid': 'AccessECS',
      'Action': [
        'ecs:List*',
        'ecs:Describe*',
        'ecs:DeregisterContainerInstance',
        'ecs:UpdateContainerInstancesState',
        'ecs:RegisterTaskDefinition',
        'ecs:CreateService',
        'application-autoscaling:PutScalingPolicy',
        'application-autoscaling:RegisterScalableTarget',
        'application-autoscaling:Describe*'
      ],
      'Effect': 'Allow',
      'Resource': [
        '*'
      ]
    },
    {
      'Sid': 'AccessBatch',
      'Action': [
        'batch:List*',
        'batch:Describe*'
      ],
      'Effect': 'Allow',
      'Resource': [
        '*'
      ]
    },
    {
      'Sid': 'AccessOpsWorks',
      'Action': [
        'opsworks:DeregisterInstance',
        'opsworks:DescribeInstances',
        'opsworks:DescribeStacks',
        'opsworks:DescribeLayers'
      ],
      'Effect': 'Allow',
      'Resource': [
        '*'
      ]
    },
    {
      'Sid': 'AccessCodeDeploy',
      'Action': [
        'codedeploy:*'
      ],
      'Effect': 'Allow',
      'Resource': [
        '*'
      ]
    },
    {
      'Sid': 'AccessGeneralS3',
      'Action': [
        's3:GetObject',
        's3:List*',
        's3:GetBucketLocation'
      ],
      'Effect': 'Allow',
      'Resource': [
        '*'
      ]
    },
    {
      'Sid': 'AccessRoute53',
      'Action': [
        'route53:ListHostedZones',
        'route53:ListResourceRecordSets',
        'route53:ChangeResourceRecordSets'
      ],
      'Effect': 'Allow',
      'Resource': [
        '*'
      ]
    },
    {
      'Sid': 'AccesS3forElasticBeanstalk',
      'Effect': 'Allow',
      'Action': [
        's3:*'
      ],
      'Resource': [
        'arn:aws:s3:::elasticbeanstalk*'
      ]
    },
    {
      'Sid': 'DockerBasedBeanstalkEnvironments',
      'Action': [
        'ecs:Poll',
        'ecs:DiscoverPollEndpoint',
        'ecs:StartTelemetrySession',
        'ecs:StartTask',
        'ecs:StopTask',
        'ecs:DescribeContainerInstances',
        'ecs:RegisterContainerInstance',
        'ecs:DeregisterContainerInstance',
        'ecs:SubmitContainerStateChange',
        'ecs:SubmitTaskStateChange'
      ],
      'Effect': 'Allow',
      'Resource': [
        '*'
      ]
    }
  ]
}

def createrole(session, ExternalId):
  path='/'
  role_name='Spotinst-Role'
  description='Spotinst Role'

  trust_policy={
    'Version': '2012-10-17',
    'Statement': [
      {
        'Effect': 'Allow',
        'Principal': {
          'AWS': 'arn:aws:iam::922761411349:root'
        },
        'Action': 'sts:AssumeRole',
        'Condition': {
          'StringEquals': {
            'sts:ExternalId': ExternalId
          }
        }
      }
    ]
  }
  try:
    IAMClient = session.client('iam')
    log.info('Creating IAM Role')
    role_response = IAMClient.create_role(
          Path=path,
          RoleName=role_name,
          AssumeRolePolicyDocument=json.dumps(trust_policy),
          Description=description,
          MaxSessionDuration=3600,
    )
    log.debug(role_response)
    return role_response
  except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'DryRunOperation':
      log.info('DryRun enabled')
      pass
    elif e.response['Error']['Code'] == 'EntityAlreadyExists':
      log.error('IAM Role Already Exists')
      role_response = IAMClient.get_role(
          RoleName=role_name
      )
      return role_response
    else:
      log.error(e)

def createpolicy(session):
  try:
    IAMClient = session.client('iam')
    log.info('Creating IAM Policy')
    policy_response = IAMClient.create_policy(
    PolicyName='Spotinst-Policy',
    PolicyDocument=json.dumps(my_managed_policy)
    )
    log.debug(policy_response)
    return policy_response
  except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'DryRunOperation':
      log.info('DryRun enabled')
      pass
    elif e.response['Error']['Code'] == 'EntityAlreadyExists':
      log.error('IAM Policy Already Exists')
      role_response = IAMClient.get_policy(
          PolicyArn='arn:aws:iam::{}:policy/{}'.format(session.client('sts').get_caller_identity().get('Account'),'Spotinst-Policy')
      )
      log.debug(role_response)
      return role_response
    else:
      log.error(e)


def attachpolicy(session, role_response, policy_response):
  try:
    IAMClient = session.client('iam')
    log.info('Attaching Policy to Role')
    attach_policy_response = IAMClient.attach_role_policy(
      RoleName=role_response['Role']['RoleName'],
      PolicyArn=policy_response['Policy']['Arn']
    )
    log.debug(attach_policy_response)
    return attach_policy_response
  except Exception as e:
      log.error(e)


if __name__ == '__main__':
  usage = 'usage: ' + sys.argv[0] + ' --profile default\n'
  ImportParser = argparse.ArgumentParser(usage)
  ImportParser.add_argument('--profile', dest='AwsProfile', required=True,
                    help='using AWS CLI config for Access keys')
  ImportParser.add_argument('-v', '--verbose', dest='VerboseMode', action='count',
                      default=int(0), help='enable verbose output (-vv for more)')
  ImportParser.add_argument('--dryrun', dest='DryrunMode', action='store_true',
                      default=False,
                      help='Show what you would happen but dont make any changes')
  options = ImportParser.parse_args()
  AwsProfile = options.AwsProfile
  DryrunMode = options.DryrunMode
  VerboseMode = options.VerboseMode

  logger.Logging().configure(VerboseMode)
  log = logger.logging.getLogger('Logger')

  try:
    session = boto3.Session(profile_name=AwsProfile)
  except botocore.exceptions.ProfileNotFound:
    log.error('No AWS credentials found - check your credentials')
    sys.exit(3)

  ExternalIdCode = randomStringwithDigits(16)
  ExternalId = 'spotinst:aws:extid:' + ExternalIdCode
  role_response = createrole(session)
  policy_response = createpolicy(session)
  attachpolicy(session, role_response, policy_response)
