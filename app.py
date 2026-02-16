import json
import boto3
import os

# Initialize the SNS client
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    # Get the SNS Topic ARN from an environment variable or hardcode it from Module 9
    # Replace 'YOUR_SNS_TOPIC_ARN' with your actual ARN from the console
    topic_arn = "arn:aws:sns:us-east-1:760659115700:ImageApp-UploadsNotificationTopic"

    try:
        # 1. Loop through the records sent by SQS
        for record in event['Records']:
            # 2. Parse the body of the SQS message
            message_body = json.loads(record['body'])
            
            # Extract image info (assuming standard S3 event structure)
            # Adjust these keys based on how your Module 10 app sends data
            image_name = message_body.get('image_name', 'Unknown Image')
            upload_time = message_body.get('upload_time', 'Unknown Time')

            print(f"Processing notification for: {image_name}")

            # 3. Create the email message
            email_subject = "New Image Uploaded!"
            email_body = (
                f"Hello,\n\n"
                f"A new image has been successfully uploaded to your app.\n\n"
                f"Image Name: {image_name}\n"
                f"Upload Time: {upload_time}\n\n"
                f"Check your S3 bucket for details."
            )

            # 4. Publish to SNS
            response = sns_client.publish(
                TopicArn=topic_arn,
                Message=email_body,
                Subject=email_subject
            )
            
            print(f"SNS Response: {response['MessageId']}")

        return {
            'statusCode': 200,
            'body': json.dumps('Notifications sent successfully!')
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing notification')
        }