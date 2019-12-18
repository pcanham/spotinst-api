#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from spotinst_sdk import SpotinstClient
import boto3
import botocore.exceptions
import time
import argparse
import json
import sys
import logger


if __name__ == '__main__':
  usage = 'usage: ' + sys.argv[0] + ' --profile default\n'
  ImportParser = argparse.ArgumentParser(usage)
  ImportParser.add_argument('--profile', dest='AwsProfile', required=True,
                    help='using AWS CLI config for Access keys')
  ImportParser.add_argument('--arn', dest='IamArn', required=True,
                    help='IAM Role ARN')
  ImportParser.add_argument('--spotinst_token', dest='spotinst_token', required=True,
                    help='Spotinst API Token')
  ImportParser.add_argument('--spotinst_accountid', dest='spotinst_accountid', required=True,
                    help='Spotinst Account ID linked to token')
  ImportParser.add_argument('-v', '--verbose', dest='VerboseMode', action='count',
                      default=int(0), help='enable verbose output (-vv for more)')
  ImportParser.add_argument('--dryrun', dest='DryrunMode', action='store_true',
                      default=False,
                      help='Show what you would happen but dont make any changes')
  options = ImportParser.parse_args()
  AwsProfile = options.AwsProfile
  spotinst_token = options.spotinst_token
  spotinst_accountid = options.spotinst_accountid
  DryrunMode = options.DryrunMode
  VerboseMode = options.VerboseMode

  logger.Logging().configure(VerboseMode)
  log = logger.logging.getLogger('Logger')

  ExternalIdCode = aws_setup.randomStringwithDigits(16)
  ExternalId = 'spotinst:aws:extid:' + ExternalIdCode

  client = SpotinstClient(auth_token=spotinst_token, account_id=spotinst_accountid)
  #account = client.create_account(AwsProfile)
  #log.debug(account)
  log.info('Setting Cloud credentials in Spotinst')
  #log.debug('Role ARN: {} ExternalId: {}'.format(role_response['Role']['Arn'], ExternalId))
  spotinst_set_cloud_creds = client.set_cloud_credentials(IamArn, ExternalId)
  log.debug(spotinst_set_cloud_creds)
