#!/usr/bin/env python
from writer import Writer

import logging
import argparse


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(module)s.%(funcName)s | %(lineno)s - '
    '%(message)s', level=logging.DEBUG)

# suppress loggers of chatty packages
logging.getLogger('boto').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('boto3.resources.action').setLevel(logging.CRITICAL)
logging.getLogger('boto3.resources.factory').setLevel(logging.CRITICAL)

args_parser = argparse.ArgumentParser(
    description='Ask for user specific information'
)

args_parser.add_argument(
    '-e',
    '--environment',
    action='store',
    dest='environment'
)

args_parser.add_argument(
    '-I',
    '--accounts-items',
    action='store_true',
    dest='accounts_items'
)

args_parser.add_argument(
    '-i',
    '--policies-items',
    action='store_true',
    dest='policies_items'
)

args_parser.add_argument(
    '-p',
    '--policies-objects',
    action='store_true',
    dest='policies_objects'
)

args_parser.add_argument(
    '-a',
    '--app-name',
    action='store',
    dest='app_name'
)
args_parser.add_argument(
    '-x',
    '--execution',
    action='store_true',
    dest='execution'
)


def main():
    user_args = args_parser.parse_args()
    policies_items = user_args.policies_items
    accounts_items = user_args.accounts_items
    policies_objects = user_args.policies_objects
    environment = user_args.environment
    app_name = user_args.app_name
    execution = user_args.execution
    writer = Writer(environment, app_name)
    if accounts_items:
        writer.account_items()
    if policies_items:
        writer.policy_items()
    if policies_objects:
        writer.policies()
    if execution:
        writer.execution_template()


if __name__ == '__main__':
    main()
