import json
import boto3

def wordCounterFunction(event, context):
    # Connect to the AWS services
    s3 = boto3.client('s3')
    sns = boto3.client('sns')

    # SNS Topic arn
    TOPIC_ARN = "arn:aws:sns:us-west-2:750816607023:WordCountTopic"

    # Get the bucket name and filename of the recently uploaded file
    bucket = event['Records'][0]['s3']['bucket']['name']
    filename = event['Records'][0]['s3']['object']['key']

    # Get the content of the uploaded file from S3
    response = s3.get_object(Bucket=bucket, Key=filename)
    content = response['Body'].read().decode('utf-8')

    # Split the contents of the file into a word list
    wordList = content.replace("\n", " ").split(" ")

    # Count number of elements in the list, i.e., number of words
    wordCount = len(wordList)

    # Output message
    message = f"The word count in the {filename} file is {wordCount}."

    # Send the SNS notification
    sns.publish(
            TopicArn=TOPIC_ARN,
            Message=message,
            Subject="✅ New Text File added to S3 bucket - Contagem de Palavras"
        )

    # This print is so you can see the message in CloudWatch logs
    print(message)

    # With this you can see the message in AWS Lambda message return
    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }