from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_s3 as s3,
)
from constructs import Construct

class FusionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        s3.CfnBucket( self, "fusion-bucket-1",bucket_name="fusion-bucket-1",
                        access_control="Private", 
                        bucket_encryption=s3.CfnBucket.BucketEncryptionProperty( 
                            server_side_encryption_configuration=[ 
                                s3.CfnBucket.ServerSideEncryptionRuleProperty( 
                                    server_side_encryption_by_default=s3.CfnBucket.ServerSideEncryptionByDefaultProperty( 
                                        sse_algorithm="AES256" ) ) ] ), 
                        public_access_block_configuration=s3.BlockPublicAccess.BLOCK_ALL,
                        tags= [{'key': 'environment', 'value': 'development'}],
                        versioning_configuration=s3.CfnBucket.VersioningConfigurationProperty(status="Enabled"))


                           
    # #   tag = s3.Tag (
    #                  key="fusion",
    #                  value="project"
    #                 )
    
   
    