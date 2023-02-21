# from aws_cdk import (
#     # Duration,
#     Stack,
#     # aws_sqs as sqs,
#     aws_lambda as _lambda,
# )
# from constructs import Construct

# class FusionSubscriberStack(Stack):

#     def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
#         super().__init__(scope, construct_id, **kwargs)

#         # The code that defines your stack goes here

#         # example resource
#         # queue = sqs.Queue(
#         #     self, "FusionSubscriberQueue",
#         #     visibility_timeout=Duration.seconds(300),
#         # )

#         # # Defines an AWS Lambda resource
#         # my_lambda = _lambda.Function(
#         #     self, 'HelloHandler',
#         #     runtime=_lambda.Runtime.PYTHON_3_7,
#         #     code=_lambda.Code.from_asset('lambda'),
#         #     handler='hello.handler',
#         # )
        


from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    # core
)
from constructs import Construct

class FusionSubscriberStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        
        s3.CfnBucket( self, "fusion-bucket-1",bucket_name="fusion-bucket-2",
                        access_control="Private", 
                        bucket_encryption=s3.CfnBucket.BucketEncryptionProperty( 
                            server_side_encryption_configuration=[ 
                                s3.CfnBucket.ServerSideEncryptionRuleProperty( 
                                    server_side_encryption_by_default=s3.CfnBucket.ServerSideEncryptionByDefaultProperty( 
                                        sse_algorithm="AES256" ) ) ] ), 
                        public_access_block_configuration=s3.BlockPublicAccess.BLOCK_ALL,
                        tags= [{'key': 'environment', 'value': 'development'}],
                        versioning_configuration=s3.CfnBucket.VersioningConfigurationProperty(status="Enabled"))


        dynamodb.CfnTable( self, "MyCfnTable", 
            key_schema=[dynamodb.CfnTable.KeySchemaProperty( 
                      attribute_name="ref_event_uid", 
                      #hash -- partition key - RANGE - sort key
                      key_type="HASH"
            )],

                # the properties below are optional
            attribute_definitions=[dynamodb.CfnTable.AttributeDefinitionProperty(
            # The data type for the attribute, where:. - S - the attribute is of type String - N - the attribute is of type Number - B - the attribute is of type Binary
                attribute_name="ref_event_uid",
                attribute_type="N"
            )],
            billing_mode="PAY_PER_REQUEST",
            # Valid values include: - PROVISIONED - We recommend using PROVISIONED for predictable workloads. PROVISIONED sets the billing mode to Provisioned Mode . - PAY_PER_REQUEST - We recommend using PAY_PER_REQUEST for unpredictable workloads. PAY_PER_REQUEST sets the billing mode to On-Demand Mode . If not specified, the default is PROVISIONED 
         
            sse_specification=dynamodb.CfnTable.SSESpecificationProperty(
                sse_enabled=True,

            #     # the properties below are optional
            #     kms_master_key_id="kmsMasterKeyId",
            #     sse_type="sseType"
             ),
            table_class="STANDARD",
            table_name="fusiondynamodbtable",
            tags= [{'key': 'environment', 'value': 'development'}],              
            
            )
