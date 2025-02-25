import pulumi
import pulumi_aws as aws

# ***Load configuration***
config = pulumi.Config("aws-cli")
instance_name = config.get("instance_name") or f"Default-Instance"
instance_type = config.get("size_type") or "t2.micro"  # שים לב לשם המשתנה כאן
ami_types = config.get("ami_types") or "Amazon Linux"

# לוודא שהמשתנים לא ריקים
if not instance_name or not instance_type or not ami_types:
    raise ValueError("All parameters (instance_name, instance_type, ami_types) must be provided.")

# ***Determine architecture based on instance type***
arch = "arm64" if instance_type.startswith("t4g") else "x86_64"

# ***Define AMIs***
ami_options = {
    "Ubuntu": aws.ec2.get_ami(
        owners=["099720109477"],
        most_recent=True,
        filters=[ 
            {"name": "name", "values": ["ubuntu/images/hvm-ssd/ubuntu-*-server-*"]},
            {"name": "architecture", "values": [arch]}
        ]
    ).id,
    "Amazon Linux": aws.ec2.get_ami(
        owners=["137112412989"],
        most_recent=True,
        filters=[ 
            {"name": "name", "values": ["amzn2-ami-hvm-*"]},
            {"name": "architecture", "values": [arch]}
        ]
    ).id
}

# ***Validate AMI choice***
if ami_types not in ami_options:
    raise ValueError(f"Invalid AMI choice: {ami_types}. Choose 'Ubuntu' or 'Amazon Linux'.")

ami_id = ami_options[ami_types]

# ***Create EC2 instance***
instance = aws.ec2.Instance(
    instance_name,
    instance_type=instance_type,  # כאן אנחנו משתמשים ב-instance_type ולא size_type
    ami=ami_id,
    tags={
        "Name": instance_name, 
        "CreatedBy": "Pulumi",
        "Owner": "elayvilkom"
    },
    opts=pulumi.ResourceOptions(
        retain_on_delete=True,
        replace_on_changes=["ami", "instance_type"],  # עדכון שם המשתנה גם כאן
        delete_before_replace=False
    )
)

# ***Export the instance ID***
pulumi.export("instance_id", instance.id)
