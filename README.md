# AWS Resource Provisioning CLI Tool

## Overview
This Python-based CLI tool automates the provisioning and management of AWS resources, allowing developers to create and manage EC2 instances, S3 buckets, and Route53 DNS records while ensuring compliance with DevOps standards.

## Features
### 1. EC2 Instance Management
- **Create EC2 Instances**: Supports only `t3.nano` and `t4g.nano` instance types.
- **AMI Selection**: Choose between the latest Ubuntu or Amazon Linux AMI.
- **Instance Limits**: Prevents creation of more than two running instances.
- **Manage Instances**: Start and stop instances, but only those created via this CLI.
- **List Instances**: Displays only instances created through this CLI.

### 2. S3 Bucket Management
- **Create S3 Buckets**: Option to set bucket access as `public` or `private`.
- **Public Bucket Confirmation**: Requires additional approval for public buckets.
- **File Upload**: Upload files only to buckets created through this CLI.
- **List Buckets**: Displays only buckets created by this CLI.

### 3. Route53 DNS Management
- **Create Hosted Zones**: Automates DNS zone creation.
- **Manage DNS Records**: Add, update, and delete DNS records, but only for zones created via this CLI.

## Installation
### Prerequisites
- Python 3.9+
- AWS CLI installed and configured (`aws configure`)
- Boto3 library installed

### Setup
```sh
# Clone the repository
git clone [<repository-url>](https://github.com/elayvilkom/PytonProject.git)
cd PytonProject

# Install dependencies
pip install -r requirements.txt
```

## Usage
### General CLI Command Format
```sh
python cli.py <resource> <action> [options]
```

### Example Commands
#### EC2 Instances
```sh
# Create an EC2 instance
python cli.py ec2 create --name my-instance --size t3.nano --ami ubuntu

# Start an EC2 instance
python cli.py ec2 start --id i-1234567890abcdef0

# Stop an EC2 instance
python cli.py ec2 stop --id i-1234567890abcdef0

# List EC2 instances
python cli.py ec2 list
```

#### S3 Buckets
```sh
# Create a private S3 bucket
python cli.py s3 create --name my-bucket --access private

# Create a public S3 bucket (requires confirmation)
python cli.py s3 create --name public-bucket --access public

# Upload a file to an S3 bucket
python cli.py s3 upload --bucket my-bucket --file path/to/file.txt

# List S3 buckets
python cli.py s3 list
```

#### Route53 DNS Records
```sh
# Create a Route53 hosted zone
python cli.py dns create-zone --name example.com

# Add a DNS record
python cli.py dns add-record --zone example.com --type A --name www --value 192.168.1.1

# Delete a DNS record
python cli.py dns delete-record --zone example.com --type A --name www
```

## Security Considerations
- **Do not expose AWS credentials in Git**: Use environment variables or AWS profiles.
- **Follow IAM best practices**: Assign least privilege permissions for resource management.
- **Public S3 Buckets**: Require confirmation to avoid unintended exposure.

## Contribution
Feel free to submit issues or pull requests to enhance the project!

## License
This project is licensed under the MIT License.

