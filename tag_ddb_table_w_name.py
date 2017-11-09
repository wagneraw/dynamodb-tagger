from __future__ import print_function
import boto3
from botocore.exceptions import ClientError
import json
import os
from sys import exit

""" Lambda function that is triggered by DDB createTables that then tags the table with whatever tags your generate_tags function returns """

def tag_table(tableName, tags):
    """take a list of tags and apply them to a table 
    tags must be a list of dicts, each dict taking the form {'Key':'keyValue', 'Value':'valueValue'}"""
    ddb_client = boto3.client('dynamodb')
    
    if not validate_tags(tags):
        print('issue with format of tags, exiting')
        sys.exit()
        
    table_arn = ddb_client.describe_table(TableName=tableName)['Table']['TableArn']
    try:
        print('tagging {} with {}'.format(tableName, tags))
        response = ddb_client.tag_resource(ResourceArn=table_arn, Tags=tags)
        #printing response for debugging purposes
        print(json.dumps(response))
    except ClientError as e:
        if e.response['Error']['Code'] == 'ValidationException':
            print('error tagging {} - already at max number of tags for table'.format(tableName))
        else:
            print("Unexpected error: {}".format(e))


def generate_tags(tableName):
    """this is the most bare bones generate_tags function that just tags it with the name"""
    tags = [{'Key':'Name', 'Value':tableName}]
    return tags


#def generate_tags(tableName):
#    """example generate_tags function that expects table names in the format baseName.project.environment
#    and then produces 3 additional tags in addition to the name tage: baseName, project, and env"""
#    components = tableName.split('.')
#    if len(components) < 3:
#        print('tablename is not in the format baseName.project.env, only applying base Name tag')
#        tags = [{'Key':'Name', 'Value':tableName}]
#        return tags
#    else:
#        env = components.pop()
#        project = components.pop()
#        baseName = str.join('.', components)
#        tags = [{'Key':'Name', 'Value':tableName}, 
#                {'Key':'Env', 'Value':env},
#                {'Key':'Project', 'Value':project},
#                {'Key':'baseName', 'Value':baseName}
#                ]
#        return tags


def validate_tags(tags):
    """makes sure the tags are well formed"""
    tags_good = True
    for tag in tags:
        if not all (key in tag for key in ('Key', 'Value')):
            print("the following tag is malformed: {}".format(tag))
            tags_good = False
    return tags_good


def handler(event, context):
    """main lambda handler"""
    #print(json.dumps(event))
    if event['detail']['eventName'] != 'CreateTable':
        print('This lambda function is meant to be triggered on DynamoDB CreateTable, recieved event: {}. exiting'.format(event['detail']['eventName']))
        exit(1)

    tableName = event['detail']['responseElements']['tableDescription']['tableName']
    tags = generate_tags(tableName)
    tag_table(tableName, tags)



