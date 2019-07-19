import boto3

rds_client = boto3.client('rds', region_name='us-east-1')

SUBNET_GROUP_NAME = 'pigLatin'

def create_db_subnet_group(subnet_group_name=SUBNET_GROUP_NAME):
    print("Creating RDS Subnet Group" + subnet_group_name)
    rds_client.create_db_subnet_group(
        DBSubnetGroupName=subnet_group_name,
        DBSubnetGroupDescription='Subnet Group for Pig Latin API',
        SubnetIds=['subnet-00000000','subnet-00000000','subnet-00000000']
    )

def create_db_secG(security_group_name='pigLatin'):
    '''create secG using ec2 client + inbound rule'''
    ec2 = boto3.client('ec2',region_name='us-east-1')
    #create secG
    security_group = ec2.create_security_group(
        GroupName=security_group_name,
        Description='Public Access RDS SecurityGrp',
        VpcId='vpc-b10096cb'
    )
    # get id of secG
    security_group_id = security_group['GroupId']

    print("Created RDS secG with id " + security_group_id)
    # add public access rule to sg ( ingress rule )
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 5432,
                'ToPort': 5432,
                'IpRanges' : [{'CidrIp':'0.0.0.0/0'}]

            }

        ]

    )
    print("Added inbound access rule to secG with group id " + security_group_id)
    return security_group_id

def launch_rds_instance():
    print("Launching AWS RDS PostgreSQL instance...")

    security_group_id = create_db_secG()

    create_db_subnet_group()
    print("Created DB Subnet Group")

    rds_client.create_db_instance(
        DBName='PigLatin',
        DBInstanceIdentifier="PigLatinID",
        DBInstanceClass="db.t2.micro",
        Engine="postgres",
        EngineVersion="10.6",
        Port=5432,
        MasterUsername="dummy",
        MasterUserPassword="dummy",
        AllocatedStorage=20,
        MultiAZ=False,
        StorageType="gp2",
        PubliclyAccessible=True,
        VpcSecurityGroupIds=[security_group_id],
        DBSubnetGroupName=SUBNET_GROUP_NAME
    )

if __name__ == '__main__':
    launch_rds_instance()

#AWS/FLASK/RDS/CRUD practice - API that returns pig latin translation of the input
#Data is written to RDS tables in AWS
#Elliott Arnold  7-19-19
#si3mshady