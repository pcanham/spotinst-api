#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import boto3
import logger
import sys
import argparse
from spotinst_sdk import SpotinstClient


if __name__ == '__main__':
  usage = 'usage: ' + sys.argv[0] + ' --profile default\n'
  ImportParser = argparse.ArgumentParser(usage)
  ImportParser.add_argument('--spotinst_token', dest='api_token', required=True,
                    help='Spotinst API Token')
  ImportParser.add_argument('--spotinst_accountid', dest='api_accountid', required=True,
                    help='Spotinst Account ID linked to token')
  ImportParser.add_argument('-v', '--verbose', dest='VerboseMode', action='count',
                      default=int(0), help='enable verbose output (-vv for more)')
  options = ImportParser.parse_args()
  api_token = options.api_token
  api_accountid = options.api_accountid
  VerboseMode = options.VerboseMode

  logger.Logging().configure(VerboseMode)
  log = logger.logging.getLogger('Logger')
  #loggers = [logger.logging.getLogger(name) for name in logger.logging.root.manager.loggerDict]
  #print(loggers)

  client = SpotinstClient(auth_token=api_token, account_id=api_accountid)
  getaccounts = client.get_accounts()
  for account in getaccounts:
    print('Account ID: {} Account Name: {}'.format(account['account_id'], account['name']))
