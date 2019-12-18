#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from spotinst_sdk import SpotinstClient
import boto3
import botocore.exceptions
import time
import argparse
import json
import sys
import aws_setup
import logger


def iter_except(func, exception, first=None):
    """ Call a function repeatedly until an exception is raised."""
    try:
        if first is not None:
            yield first()            # For database APIs needing an initial cast to db.first()
        while True:
            yield func()
    except exception:
        pass


if __name__ == '__main__':
  usage = 'usage: ' + sys.argv[0] + ' --profile default\n'
  ImportParser = argparse.ArgumentParser(usage)
  ImportParser.add_argument('--profile', dest='AwsProfile', required=True,
                    help='using AWS CLI config for Access keys')
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

  try:
    session = boto3.Session(profile_name=AwsProfile)
  except botocore.exceptions.ProfileNotFound:
    log.error('No AWS credentials found - check your credentials')
    sys.exit(3)

  aws_setup.VerboseMode = VerboseMode
  ExternalIdCode = aws_setup.randomStringwithDigits(16)
  ExternalId = 'spotinst:aws:extid:' + ExternalIdCode
  role_response = aws_setup.createrole(session, ExternalId)
  log.debug(role_response)
  policy_response = aws_setup.createpolicy(session)
  log.debug(policy_response)
  attach_response = aws_setup.attachpolicy(session, role_response, policy_response)
  log.debug(attach_response)

  client = SpotinstClient(auth_token=spotinst_token, account_id=spotinst_accountid)
  account = client.create_account(AwsProfile)
  log.debug(account)
  log.info('Setting Cloud credentials in Spotinst')
  log.debug('Role ARN: {} ExternalId: {}'.format(role_response['Role']['Arn'], ExternalId))
  new_client = SpotinstClient(auth_token=spotinst_token, account_id=account['id'])

  sleep_time = 2
  num_retries = 4

  for x in range(0, num_retries):
    try:
      spotinst_set_cloud_creds = new_client.set_cloud_credentials(role_response['Role']['Arn'], ExternalId)
    except:
      spotinst_set_cloud_creds = None
      y = x+1
      log.warning('set_cloud_credentials produced an exception, retrying on attempt {} of {}'.format(y, num_retries))
      pass
    if spotinst_set_cloud_creds is None:
      time.sleep(sleep_time)  # wait before trying to fetch the data again
      sleep_time *= 2  # Implement your backoff algorithm here i.e. exponential backoff
    else:
      break
  log.info('set_cloud_credentials completed for {}'.format(AwsProfile))
  log.debug(spotinst_set_cloud_creds)
