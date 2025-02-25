import pulumi
import pulumi_aws as aws
import boto3
import json
from tabulate import tabulate
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import ClientError
import os
import logging



def choose_s3():
    while True:
        bucket_name = input("Enter the name of the S3 bucket you want: ")

        print("\n🔹 Choose the S3 bucket type:")
        print("1️⃣  Public")
        print("2️⃣  Private")
        acl_choice = input("👉 Enter choice (1 or 2): ")
        
        if acl_choice == "1":
            sure = input("Are you sure? (yes/no): ").lower()
            if sure == "yes":
                acl_s3 = "public"
                break
        elif acl_choice == "2":
            acl_s3 = "private"
            break
        else:
            print("❌ Invalid input! Please enter 1 or 2.")

    print(f"✅ Your choice for S3 bucket: {acl_s3}")
    return acl_s3, bucket_name

def create_s3(acl_s3, bucket_name):
    s3_client = boto3.client('s3')
    try:
        # יצירת ה-Bucket
        response = s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'us-west-1'}
        )

        print(f"🚀 Bucket '{bucket_name}' is now up and running!")

        # אם המשתמש ביקש דלי ציבורי, נוסיף לו מדיניות גישה ציבורית
        if acl_s3 == "public":
            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "PublicReadGetObject",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{bucket_name}/*"
                    }
                ]
            }
            
            s3_client.put_bucket_policy(
                Bucket=bucket_name,
                Policy=json.dumps(policy)
            )
            print("🌍 Public access policy applied!")

    except Exception as e:
        print(f"❌ Error creating the S3 bucket: {e}")
        
def list_s3_buckets():
    """פונקציה שמחזירה רשימה של כל ה-S3 Buckets בחשבון AWS ומציגה בטבלה"""
    s3_client = boto3.client("s3")

    try:
        response = s3_client.list_buckets()
        buckets = response.get("Buckets", [])

        if not buckets:
            print("📭 No S3 buckets found!")
            return

        # יצירת רשימה מסודרת להצגה עם tabulate
        table_data = [[i + 1, bucket["Name"], bucket["CreationDate"]] for i, bucket in enumerate(buckets)]
        headers = ["#", "Bucket Name", "Creation Date"]

        print("\n📋 List of S3 Buckets:")
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    except Exception as e:
        print(f"❌ Error retrieving S3 buckets: {e}")

def uploud_file_s3():
    file_name = input("enter the file name: ")
    bucket_name = input("enter the bucket name:")
    object_name = os.path.basename(file_name)
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_s3():
    s3_client = boto3.client('s3')
    bucket_name = input("enter the name of the bucket the you whant to delete")
    try:
        s3_client.delete_bucket(Bucket=bucket_name)
    except Exception as e:
        print(f"the was a erorr {e}")
