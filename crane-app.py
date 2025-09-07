import boto3
import os
import subprocess
import base64
import json
import traceback
import tempfile

def assume_role(role_arn):
    sts = boto3.client('sts')
    creds = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName='ECRCopySession'
    )['Credentials']
    return boto3.Session(
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretAccessKey'],
        aws_session_token=creds['SessionToken']
    )

def crane_login(registry, token, docker_config_dir):
    env = os.environ.copy()
    env["DOCKER_CONFIG"] = docker_config_dir  

    login_cmd = [
        'crane', 'auth', 'login', registry,
        '-u', 'AWS',
        '-p', token
    ]
    result = subprocess.run(login_cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        raise Exception(f"Crane login failed for {registry}:\n{result.stderr}")
    else:
        print(f"Crane login succeeded for {registry}")

def lambda_handler(event, context):
    repo = "unknown"
    try:
        print("Event:", json.dumps(event))

        # Get ECR clients
        source_ecr = boto3.client('ecr', region_name=os.environ['SOURCE_REGION'])
        dest_session = assume_role(os.environ['DEST_ROLE_ARN'])
        dest_ecr = dest_session.client('ecr', region_name=os.environ['DEST_REGION'])

        # Writable Docker config dir
        docker_config_dir = tempfile.mkdtemp(dir='/tmp')

        # Detect repository
        if 'repository' in event:
            repo = event['repository']['S'] if isinstance(event['repository'], dict) else event['repository']
        elif 'repositoryName' in event:
            repo = event['repositoryName']
        elif isinstance(event, str):
            repo = event
        else:
            repo = str(event)

        print(f"Repository: {repo}")

        source_registry = f"{os.environ['SOURCE_ACCOUNT_ID']}.dkr.ecr.{os.environ['SOURCE_REGION']}.amazonaws.com"
        dest_registry = f"{os.environ['DEST_ACCOUNT_ID']}.dkr.ecr.{os.environ['DEST_REGION']}.amazonaws.com"

        # Create destination repo if needed
        try:
            dest_ecr.create_repository(repositoryName=repo)
            print(f" Created repository: {repo}")
        except dest_ecr.exceptions.RepositoryAlreadyExistsException:
            print(f" Repository already exists: {repo}")

        # Get auth tokens
        source_auth = source_ecr.get_authorization_token()['authorizationData'][0]
        dest_auth = dest_ecr.get_authorization_token()['authorizationData'][0]

        source_token = base64.b64decode(source_auth['authorizationToken']).decode().split(':')[1]
        dest_token = base64.b64decode(dest_auth['authorizationToken']).decode().split(':')[1]

        # Crane logins
        crane_login(source_registry, source_token, docker_config_dir)
        crane_login(dest_registry, dest_token, docker_config_dir)

        # Paginate images
        paginator = source_ecr.get_paginator('list_images')
        copied_images = []

        for page in paginator.paginate(repositoryName=repo):
            for image in page['imageIds']:
                tag = image.get('imageTag') or image.get('imageDigest')
                if not tag:
                    continue

                source_uri = f"{source_registry}/{repo}:{tag}"
                dest_uri = f"{dest_registry}/{repo}:{tag}"

                print(f" Copying {source_uri} to {dest_uri}")

                # Set env for crane
                env = os.environ.copy()
                env["DOCKER_CONFIG"] = docker_config_dir

                result = subprocess.run([
                    'crane', 'copy', source_uri, dest_uri
                ], capture_output=True, text=True, env=env)

                print(" Crane stdout:", result.stdout)
                if result.stderr:
                    print(" Crane stderr:", result.stderr)

                if result.returncode == 0:
                    copied_images.append(f"{repo}:{tag}")
                    print(f" Successfully copied: {repo}:{tag}")
                else:
                    print(f" Failed to copy: {tag}")

        return {
            "status": "success",
            "repository": repo,
            "copied_images": copied_images,
            "total_images": len(copied_images)
        }

    except Exception as e:
        print(f" Unexpected error: {str(e)}")
        traceback.print_exc()
        try:
            sns = boto3.client('sns')
            sns.publish(
                TopicArn=os.environ['NOTIFY_TOPIC'],
                Message=f" Failed to copy repository {repo}: {str(e)}"
            )
        except Exception as sns_error:
            print(f" Failed to send SNS notification: {sns_error}")
        raise
