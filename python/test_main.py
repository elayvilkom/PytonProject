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
while True:
    print("\n🔹 Welcome to AWS Management CLI 🔹")
    print("1️⃣. EC2 Instance\n2️⃣. S3 Bucket\n3️⃣. Route 53\n4️⃣. Exit\n👉 Please choose an option (1, 2, 3 or 4): ")
    choose = input()
    print (choose)
    if choose == "1":
        print("\n🔹 EC2 Instance Management 🔹")
        choose_ec2 = input("1️⃣. Create EC2\n2️⃣. Manage EC2\n0️⃣. Go Back\n👉 Choose an option: ")
        if choose == '1':
            catalog_choice()  # קריאה לפונקציה שיצרת