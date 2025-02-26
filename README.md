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
git clone https://github.com/elayvilkom/PytonProject.git
cd PytonProject

# Install dependencies
pip install -r requirements.txt
```

## Security Considerations
- **Do not expose AWS credentials in Git**: Use environment variables or AWS profiles.
- **Follow IAM best practices**: Assign least privilege permissions for resource management.
- **Public S3 Buckets**: Require confirmation to avoid unintended exposure.

