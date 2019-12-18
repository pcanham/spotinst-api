#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import boto3
import logger
import sys
import argparse
from spotinst_sdk import SpotinstClient


if __name__ == '__main__':
  usage = 'usage: ' + sys.argv[0] + ' --spotinst_token blahblah --spotinst_accountid blah --del_accountid blahblah\n'
  ImportParser = argparse.ArgumentParser(usage)
  ImportParser.add_argument('--spotinst_token', dest='api_token', required=True,
                    help='Spotinst API Token')
  ImportParser.add_argument('--spotinst_accountid', dest='api_accountid', required=True,
                    help='Spotinst Account ID linked to token')
  ImportParser.add_argument('--del_accountid', dest='SpotinstAccount', required=True,
                      help='Spotinst Account Name displayed in console')
  ImportParser.add_argument('-v', '--verbose', dest='VerboseMode', action='count',
                      default=int(0), help='enable verbose output (-vv for more)')
  options = ImportParser.parse_args()
  api_token = options.api_token
  api_accountid = options.api_accountid
  SpotinstAccount = options.SpotinstAccount
  VerboseMode = options.VerboseMode

  logger.Logging().configure(VerboseMode)
  log = logger.logging.getLogger('Logger')

  client = SpotinstClient(auth_token=api_token, account_id=api_accountid)
  client.delete_account(SpotinstAccount)
