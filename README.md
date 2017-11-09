# DynamoDB-Tagger

DynamoDB-Tagger is a sample project that automates the tagging of new DynamoDB tables. The project makes use of a Lambda function that tags a DynamoDB table with it's name. The function is triggered by a Cloud Watch Event Rule every time a new DynamoDB table is created. Optionally you can replace the default tag generation function with one that creates additional tags based on parsing the name. The advantage to tagging your DynamoDB tables is that it allows you to easily break down your DynamoDB costs per table when viewed in Cost Explorer or in the Detailed Billing Report. 

## Getting Started

To get started, clone this repository locally:

```
$ git clone https://github.com/wagneraw/dynamodb-tagger
```

### Prerequisites

To run DynamoDB-Tagger, you will need to:

1. Select an AWS Region into which you will deploy services. Be sure that all required services (AWS Lambda and  AWS CloudWatch Events) are available in the Region you select.
2. Confirm your [installation of the latest AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/installing.html) (at least version 1.11.21).
3. Confirm the [AWS CLI is properly configured](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration).
4. Choose an existing S3 bucket in the region you chose or [create a new one](http://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html), the bucket will only be used to store the deployment templates.

## Deploying the solution

The project uses [AWS Serverless Application Model(SAM)](http://docs.aws.amazon.com/lambda/latest/dg/deploying-lambda-apps.html#serverless_app) to deploy the Lambda function and CloudWatch Event.

1. Using SAM, package the source code and create the deployment template:

  ```
  $ aws cloudformation --region <REGION> package --template-file template.yaml --output-template-file deploy-template.yaml --s3-bucket <MY_S3_BUCKET>
  ```

2. Once the packaging is complete deploy the deployment template:

  ```
  $ aws cloudformation --region <REGION> deploy --template-file deploy-template.yaml --stack-name dynamodb-tagger --capabilities CAPABILITY_IAM
  ```

3. That's it, the next time you create a DynamoDB table in this region the CloudWatch Event Rule will trigger the Lambda function which will add the Name tag to the table.

4. (Optional) - If you use a naming convention for your DynamoDB tables you can write a custom tag generator to add additional tags based on parsing the name. An example is included, it's commented out, that handles table names in the format baseName.Project.Environment.

## Cleaning up

To delete the Lambda function and the CloudWatch Event Rule simply delete the stack:

```
$ aws cloudformation --region <REGION> delete-stack --stack-name dynamodb-tagger
```

## Authors

* **Adam Wagner**
