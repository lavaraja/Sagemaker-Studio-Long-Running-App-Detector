import boto3
from datetime import datetime, timedelta,timezone
import time
import math

Region="Your-Region"
DomainId="Your-Domain"
UserProfile='Your-User-Profile'
sns_topic_arn = 'YOUR_SNS_TOPIC_ARN'  # Replace with your SNS topic ARN

# Create a boto3 client for SageMaker
client = boto3.client('sagemaker',region_name=Region)

# Define the time interval for idle detection (e.g., 240 minutes, 4 hours)
idle_threshold = timedelta(minutes=240) # change the idle_threshold as per your needs and specify in minutes. For ex: 1 days = 1440 mins

# Create an SNS client
sns_client = boto3.client('sns',"us-east-1")

def get_userprofile_for_domain(DomainId):
    response=client.list_user_profiles(DomainIdEquals=DomainId,MaxResults=100)
    user_profiles=response["UserProfiles"]
    return user_profiles

def get_apps_for_user(DomainId,UserProfile):
    response = client.list_apps(UserProfileNameEquals=UserProfile,DomainIdEquals=DomainId,MaxResults=100)
    return response

def get_list_of_all_apps():
    apps=[]
    if DomainId and UserProfile:        
        apps=get_apps_for_user(DomainId,UserProfile)
    elif DomainId and not UserProfile:
        user_profiles=get_userprofile_for_domain(DomainId)
        for up_dm in user_profiles:
            response=get_apps_for_user(up_dm["DomainId"],up_dm["UserProfileName"])
            apps.extend(response["Apps"])
    else:
        if UserProfile and not DomainId:
            assert DomainId,"Please provide DomainId when providing UserProfile"
        
    return apps

apps=get_list_of_all_apps()

for app in apps:
    if app['AppType']!="default" and app['Status']=="InService":
        #app_description = client.describe_app(AppName=app['AppName'], UserProfileName=app['UserProfileName'],DomainId=DomainId,AppType="KernelGateway")
        app_creation_time = app['CreationTime'].replace(tzinfo=None)
        #print("app_creation_time",app_creation_time)
        current_time = datetime.now(timezone.utc).replace(tzinfo=None)
        #print("current_time",current_time)
        idle_duration = current_time - app_creation_time
        print("Studio App Age is:",idle_duration," AppType:",app['AppType'])
    
        if idle_duration > idle_threshold:
            print(f"The Studio App '{app['AppName']}' under the domain '{app['DomainId']} / Userprofile '{app['UserProfileName']} is older than the threshold limit {idle_threshold} minutes. Delete the app to save costs if not being used")
            message = f"The Studio App '{app['AppName']}' under the domain '{app['DomainId']} / Userprofile '{app['UserProfileName']} is older than the threshold limit {idle_threshold} minutes. Delete the app to save costs if not being used")
            print(message)
            sns_client.publish(TopicArn=sns_topic_arn, Message=message, Subject=f"!!Long running Sagemaker Studio App detected Used by '{app['DomainId']} / Userprofile '{app['UserProfileName']}. [Action Required]")
