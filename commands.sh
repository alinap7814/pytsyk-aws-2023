
#!/bin/bash

# apt-get update

# apt-get install jq -y

# pip install --upgrade pip

# pip install -r requirements.txt

VERSION="3d14d42"

ENVIRONMENT="prod"

# CI_COMMIT_REF_NAME="v00"
# [[ $CI_COMMIT_REF_NAME = v* ]] && ENVIRONMENT="prod" && VERSION="$CI_COMMIT_REF_NAME"

# [[ $CI_COMMIT_REF_NAME = rc* ]] && ENVIRONMENT="test" && VERSION="$CI_COMMIT_REF_NAME"

ACCOUNTS_KWARGS='
{ 
    "administrator_account": "563014625035", 
    "execution_role_name": "LaunchPadOperationsStackSetExecutionRole",
    "administrator_role": "LaunchPadOperationsStackSetAdministrationRole" 
}'

KWARGS='
{ 
    "version": "'"$VERSION"'", 
    "environment": "'"$ENVIRONMENT"'", 
    "session_kwargs": { 
        "region_name": "us-east-1"
    } 
}'

EXECUTION_KWARGS=$(echo $KWARGS $ACCOUNTS_KWARGS | jq -s add)

python deployment -k "$KWARGS" -I

# RELEASE_CANDIDATE="$VERSION"
# RELEASE="${RELEASE_CANDIDATE/rc/v}"

# echo $RELEASE