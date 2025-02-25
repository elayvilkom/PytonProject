from instance import catalog_choice 
from instance import start_ec2 
from instance import stop_ec2  
from instance import delete_ec2 
from instance import list_ec2

from s3 import choose_s3
from s3 import create_s3
from s3 import list_s3_buckets
from s3 import uploud_file_s3
from s3 import delete_s3

from rout53 import create_dns_zone
from rout53 import delete_dns_zone
from rout53 import list_hosted_zones
from rout53 import create_dns_record
from rout53 import delete_dns_record
from rout53 import update_dns_record
from rout53 import list_dns_records

if __name__ == "__main__":

    while True:
        print("\n🔹 Welcome to AWS Management CLI 🔹")
        print("1️⃣. EC2 Instance\n2️⃣. S3 Bucket\n3️⃣. Route 53\n4️⃣. Exit\n👉 Please choose an option (1, 2, 3 or 4): ")
        choose = input()
        
        if choose == '2':
            print("\n🔹 S3 Bucket Management 🔹")
            choose = input("1️⃣. Create S3 Bucket\n2️⃣. List S3 Buckets\n3️⃣. Upload File to S3\n4️⃣. Delete S3 Bucket\n0️⃣. Go Back\n👉 Choose an option: ")
            if choose == '1':
                acl_s3, bucket_name = choose_s3()
                create_s3(acl_s3, bucket_name)
            elif choose == '2':
                list_s3_buckets()
            elif choose == '3':
                uploud_file_s3()
            elif choose == '4':
                delete_s3()
            elif choose == '0':
                continue
            else:
                print("❌ Invalid choice, try again.")
        
        elif choose == '1':
            print("\n🔹 EC2 Instance Management 🔹")
            choose = input("1️⃣. Create EC2\n2️⃣. Manage EC2\n0️⃣. Go Back\n👉 Choose an option: ")
            if choose == '1':
                catalog_choice()  # קריאה לפונקציה שיצרת
            elif choose == '2':
                print("\n🔹 EC2 Instance Actions 🔹")
                choose = input("1️⃣. Start EC2\n2️⃣. Stop EC2\n3️⃣. Delete EC2\n4️⃣. List EC2\n0️⃣. Go Back\n👉 Choose an option: ")
                if choose == '1':
                    start_ec2()
                elif choose == '2':
                    stop_ec2()
                elif choose == '3':
                    delete_ec2()
                elif choose == '4':
                    list_ec2()
                elif choose == '0':
                    continue
                else:
                    print("❌ Invalid choice, try again.")
            elif choose == '0':
                continue
            else:
                print("❌ Invalid choice, try again.")

        elif choose == '3':
            print("\n🔹 Route 53 Management 🔹")
            choose = input("1️⃣. Manage DNS Zone\n2️⃣. Manage DNS Records\n0️⃣. Go Back\n👉 Choose an option: ")
            if choose == '1':
                print("\n🔹 DNS Zone Management 🔹")
                choose = input("1️⃣. Create DNS Zone\n2️⃣. Delete DNS Zone\n3️⃣. List DNS Zones\n0️⃣. Go Back\n👉 Choose an option: ")
                if choose == '1':
                    create_dns_zone()
                elif choose == '2':
                    delete_dns_zone()
                elif choose == '3':
                    list_hosted_zones()
                elif choose == '0':
                    continue
                else:
                    print("❌ Invalid choice, try again.")
            elif choose == '2':
                print("\n🔹 DNS Record Management 🔹")
                choose = input("1️⃣. Create DNS Record\n2️⃣. Delete DNS Record\n3️⃣. Update DNS Record\n4️⃣. List DNS Records\n0️⃣. Go Back\n👉 Choose an option: ")
                if choose == '1':
                    create_dns_record()  # קריאה לפונקציה
                elif choose == '2':
                    delete_dns_record()
                elif choose == '3':
                    update_dns_record()
                elif choose == '4':
                    list_dns_records()
                elif choose == '0':
                    continue
                else:
                    print("❌ Invalid choice, try again.")
            elif choose == '0':
                continue
            else:
                print("❌ Invalid choice, try again.")

        elif choose == '4':
            print("👋 Goodbye! Exiting the program.")
            break
        else:
            print("❌ Invalid choice, please choose a valid option (1, 2, 3, or 4).")
