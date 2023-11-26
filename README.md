# Sagemaker Studio Long-Running App Detector

This script is designed to help cloud administrators detect long-running apps in Amazon Sagemaker Studio. It identifies idle kernel apps and sends notifications to the specified SNS topic, allowing administrators to take action and potentially save costs by deleting unused apps.

## Features

- Detects idle kernel apps based on a specified threshold.
- Sends notifications to an SNS topic for long-running apps.
- Can be scheduled to run periodically using a scheduler (e.g., AWS EventBridge and AWS Lambda).

## Purpose and Benefits

The current Jupyter plugin for [auto-shutdown](https://github.com/aws-samples/sagemaker-studio-auto-shutdown-extension/blob/main/README.md) does not continue polling for idle apps and shutting them down if the Jupyter server is restarted using the "restart-jupyter-server" command. This script provides an alternative solution to address this limitation and detect if autoshut down is disabled, ensuring that idle apps are still identified and action can be taken as needed.


## Prerequisites

- Python 3.6 or higher
- Boto3 library
- AWS credentials with appropriate permissions.

`IAM` roles permissions:

``
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "LambdaRolePermissions",
			"Effect": "Allow",
			"Action": [
				"sagemaker:ListApps",
				"sns:Publish",
				"sagemaker:ListDomains",
				"sagemaker:ListUserProfiles"
			],
			"Resource": "*"
		}
	]
}
``

## Configuration

Before using the script, ensure the following configurations are set:

1. Set the `Region`, `DomainId`, `UserProfile`, and `sns_topic_arn` variables to the appropriate values.
2. Ensure that the AWS credentials used by the script have the necessary permissions to interact with Sagemaker and SNS.

## Usage

1. Clone the repository to your local environment.
2. Modify the script with your specific configurations.
3. Run the script using `python sm_studio_app_detector.py`.

## Scheduled Execution

To run the script periodically, you can use AWS Lambda and EventBridge to schedule the execution at regular intervals. This ensures that the script continues to monitor and detect long-running apps even if the Jupyter server is restarted.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
