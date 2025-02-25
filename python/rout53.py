import boto3
from tabulate import tabulate

def create_dns_zone():
    # קבלת שם הדומיין מהמשתמש
    domain_name = input("📌 Enter the domain name (e.g., example.com): ").strip()

    # שאלת המשתמש אם מדובר באזור ציבורי או פרטי
    print("\n🔹 Choose the DNS zone type:")
    print("1️⃣  Public")
    print("2️⃣  Private")
    
    try:
        zone_type_choice = int(input("👉 Enter choice (1 or 2): "))  # המרת קלט למספר
        if zone_type_choice == 1:
            private_zone = False  # אזור ציבורי
        elif zone_type_choice == 2:
            private_zone = True  # אזור פרטי
        else:
            print("❌ Invalid input. Defaulting to 'Public'.")
            private_zone = False
    except ValueError:
        print("❌ Invalid input. Defaulting to 'Public'.")
        private_zone = False

    # יצירת לקוח Route 53
    route53_client = boto3.client('route53')

    try:
        # יצירת Hosted Zone
        response = route53_client.create_hosted_zone(
            Name=domain_name,
            CallerReference=str(hash(domain_name)),
            HostedZoneConfig={
                'Comment': 'Created via Boto3',
                'PrivateZone': private_zone
            }
        )
        
        print(f"✅ Hosted Zone '{domain_name}' created successfully!")
        print(response)

    except Exception as e:
        print(f"❌ Error: {e}")

def delete_dns_zone():
    # Get the Hosted Zone ID from the user
    zone_id = input("📌 Enter the Hosted Zone ID to delete: ").strip()

    route53_client = boto3.client('route53')

    try:
        # Delete the Hosted Zone
        response = route53_client.delete_hosted_zone(
            Id=zone_id
        )

        print(f"✅ Successfully deleted Hosted Zone with ID: {zone_id}")
        print(response)

    except Exception as e:
        print(f"❌ An error occurred: {e}. Please try again.")

def delete_dns_record():
    # קבלת פרטי ה-Hosted Zone ורשומת ה-DNS
    zone_id = input("📌 Enter the Hosted Zone ID: ")
    record_name = input("📌 Enter the record name to delete: ")

    # יצירת לקוח Route 53
    route53_client = boto3.client('route53')

    try:
        # שליפת כל הרשומות ב-zone
        response = route53_client.list_resource_record_sets(
            HostedZoneId=zone_id
        )

        # חיפוש הרשומה המתאימה לפי שם הרשומה
        record_to_delete = None
        for record in response['ResourceRecordSets']:
            if record['Name'].strip('.') == record_name:
                record_to_delete = record
                break

        if not record_to_delete:
            print(f"❌ DNS record '{record_name}' not found!")
            return

        # מחיקת הרשומה שנמצאה
        response = route53_client.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'DELETE',
                        'ResourceRecordSet': record_to_delete
                    }
                ]
            }
        )

        print(f"✅ DNS record '{record_name}' deleted successfully!")
        print(response)

    except Exception as e:
        print(f"❌ Error: {e}")

def list_hosted_zones():
    route53_client = boto3.client('route53')

    try:
        response = route53_client.list_hosted_zones()

        if not response['HostedZones']:
            print("❌ No Hosted Zones found.")
            return

        # יצירת רשימה מסודרת עם ID ושם הדומיין
        table_data = [
            [zone['Id'].split('/')[-1], zone['Name']]
            for zone in response['HostedZones']
        ]

        # הדפסת הטבלה בצורה יפה
        print("\n🔹 Available Hosted Zones:\n")
        print(tabulate(table_data, headers=["Hosted Zone ID", "Domain Name"], tablefmt="grid"))

    except Exception as e:
        print(f"❌ Error: {e}")

def create_dns_record():
    zone_id = input("📌 Enter the Hosted Zone ID: ")
    record_name = input("📌 Enter the record name: ")
    record_value = input("📌 Enter the record value: ")

    print("\n🔹 Choose the record type:")
    print("1️⃣  AAAA")
    print("2️⃣  A")
    
    try:
        record_type_choice = int(input("👉 Enter choice (1 or 2): "))  # המרת קלט למספר
        if record_type_choice == 1:
            record_type = "AAAA"
        elif record_type_choice == 2:
            record_type = "A"
        else:
            print("❌ Invalid input. Defaulting to 'A'.")
            record_type = "A"
    except ValueError:
        print("❌ Invalid input. Defaulting to 'A'.")
        record_type = "A"

    # יצירת לקוח Route 53
    route53_client = boto3.client('route53')

    try:
        response = route53_client.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'CREATE',
                        'ResourceRecordSet': {
                            'Name': record_name,
                            'Type': record_type,
                            'TTL': 300,
                            'ResourceRecords': [{'Value': record_value}]
                        }
                    }
                ]
            }
        )
        print("✅ DNS record created successfully!")
        print(response)
    except Exception as e:
        print(f"❌ Error: {e}")

def update_dns_record():
    route53_client = boto3.client('route53')

    # Get user input
    zone_id = input("📌 Enter the Hosted Zone ID: ")
    record_name = input("📌 Enter the record name (e.g., sub.example.com): ")
    new_value = input("📌 Enter the new record value: ")

    print("\n🔹 Choose the record type:")
    print("1️⃣  AAAA (IPv6)")
    print("2️⃣  A (IPv4)")

    try:
        record_type_choice = int(input("👉 Enter choice (1 or 2): "))
        record_type = "AAAA" if record_type_choice == 1 else "A"
    except ValueError:
        print("❌ Invalid input. Defaulting to 'A'.")
        record_type = "A"

    try:
        response = route53_client.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': record_name,
                            'Type': record_type,
                            'TTL': 300,
                            'ResourceRecords': [{'Value': new_value}]
                        }
                    }
                ]
            }
        )

        print(f"✅ Successfully updated {record_name} to {new_value}!")
        print(response)

    except Exception as e:
        print(f"❌ Error: {e}")

def list_dns_records():
    route53_client = boto3.client('route53')

    # Get Hosted Zone ID from user
    zone_id = input("📌 Enter the Hosted Zone ID: ")

    try:
        # Fetch the records in the Hosted Zone
        response = route53_client.list_resource_record_sets(
            HostedZoneId=zone_id
        )

        if not response['ResourceRecordSets']:
            print("❌ No DNS records found in this Hosted Zone.")
            return

        # Prepare data for the table
        table_data = [
            [record['Name'], record['Type'], record.get('TTL', 'N/A'), ', '.join([r['Value'] for r in record.get('ResourceRecords', [])])]
            for record in response['ResourceRecordSets']
        ]

        print("\n🔹 DNS Records in Hosted Zone:")
        print(tabulate(table_data, headers=["Record Name", "Record Type", "TTL", "Values"], tablefmt="grid"))

    except Exception as e:
        print(f"❌ Error: {e}")

    route53_client = boto3.client('route53')

    # Get user input
    zone_id = input("📌 Enter the Hosted Zone ID: ")
    record_name = input("📌 Enter the record name (e.g., sub.example.com): ")

    print("\n🔹 Choose the record type:")
    print("1️⃣  AAAA (IPv6)")
    print("2️⃣  A (IPv4)")

    try:
        record_type_choice = int(input("👉 Enter choice (1 or 2): "))
        record_type = "AAAA" if record_type_choice == 1 else "A"
    except ValueError:
        print("❌ Invalid input. Defaulting to 'A'.")
        record_type = "A"

    try:
        # Performing the DELETE action to remove the record
        response = route53_client.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'DELETE',
                        'ResourceRecordSet': {
                            'Name': record_name,
                            'Type': record_type,
                            'TTL': 300,
                            'ResourceRecords': [{'Value': ''}]  # Empty to delete
                        }
                    }
                ]
            }
        )

        print(f"✅ Successfully deleted record {record_name}!")
        print(response)

    except Exception as e:
        print(f"❌ Error: {e}")

