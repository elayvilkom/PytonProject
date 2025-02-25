import pulumi
import pulumi_aws as aws
import boto3
import os
from tabulate import tabulate

def catalog_choice():
    """פונקציה לבחירת פרטי ה-EC2 על ידי המשתמש עם תפריט מספרי"""
    
    instance_name = input("🔹 Enter the name of the EC2: ")

    # בחירת מספר השרתים
    while True:
        print("\n🔹 How many EC2 instances do you want? (Max 2)")
        print("1️⃣  One Instance")
        print("2️⃣  Two Instances")
        instances = input("👉 Enter choice (1 or 2): ")
        if instances in ["1", "2"]:
            instances = int(instances)
            break
        else:
            print("❌ Invalid input! Please enter 1 or 2.")

    # בחירת סוג מערכת הפעלה
    while True:
        print("\n🔹 Which type of EC2 to create?")
        print("1️⃣  Ubuntu")
        print("2️⃣  Amazon Linux")
        ami_choice = input("👉 Enter choice (1 or 2): ")
        if ami_choice == "1":
            ami_types = "ubuntu"
            break
        elif ami_choice == "2":
            ami_types = "amazon linux"
            break
        else:
            print("❌ Invalid input! Please enter 1 or 2.")

    # בחירת סוג המכונה
    while True:
        print("\n🔹 Which type of instance do you want?")
        print("1️⃣  t3.nano")
        print("2️⃣  t4g.nano")
        size_choice = input("👉 Enter choice (1 or 2): ")
        if size_choice == "1":
            size_type = "t3.nano"
            break
        elif size_choice == "2":
            size_type = "t4g.nano"
            break
        else:
            print("❌ Invalid input! Please enter 1 or 2.")

    # שמירת ההגדרות ב-Pulumi
    os.system(f"pulumi config set aws-cli:instance_name {instance_name}")
    os.system(f"pulumi config set aws-cli:size_type {size_type}")
    os.system(f"pulumi config set aws-cli:ami_types {ami_types}")

    print("\n✅ Now you need to run `pulumi up` and the instance will be created!")
    return size_type, ami_types, instance_name

def delete_ec2():
    """פונקציה למחיקת EC2 Instance"""
    ec2 = boto3.resource('ec2')
    instance_id = input("Please enter the instance ID to delete: ").strip()
    try:
        instance = ec2.Instance(instance_id)
        instance.stop()
        instance.wait_until_stopped()
        print(f"🛑 Instance {instance_id} has been stopped.")

        instance.terminate()
        instance.wait_until_terminated()
        print(f"✅ Instance {instance_id} has been terminated.")
    except Exception as e:
        print(f"An error occurred: {e}. Please try again.")

def stop_ec2():
    """פונקציה לכיבוי EC2 Instance"""
    ec2 = boto3.resource('ec2')
    instance_id = input("Please enter the instance ID to stop: ").strip()
    try:
        instance = ec2.Instance(instance_id)
        instance.stop()
        instance.wait_until_stopped()
        print(f"🛑 Instance {instance_id} has been stopped.")
    except Exception as e:
        print(f"An error occurred: {e}. Please try again.")
        stop_ec2()

def start_ec2():
    """פונקציה להפעלת EC2 Instance"""
    ec2 = boto3.resource('ec2')
    instance_id = input("Please enter the instance ID to start: ").strip()
    try:
        instance = ec2.Instance(instance_id)
        instance.start()
        instance.wait_until_running()
        print(f"✅ Instance {instance_id} has been started.")
    except Exception as e:
        print(f"An error occurred: {e}. Please try again.")
        start_ec2()

def list_ec2():
    """פונקציה להצגת כל ה-Instances עם התגית 'Owner: Elay'"""
    ec2 = boto3.client('ec2')

    response = ec2.describe_instances(
        Filters=[{'Name': 'tag:Owner', 'Values': ['elayvilkom']}]
    )

    instances_data = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']
            state = instance['State']['Name']
            
            # חיפוש תגית שם השרת
            name = "N/A"
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        name = tag['Value']
            
            instances_data.append([instance_id, name, instance_type, state])

    # הדפסת הטבלה
    headers = ["Instance ID", "Name", "Type", "Status"]
    print(tabulate(instances_data, headers=headers, tablefmt="grid"))
