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
    aws_opensearchservice as opensearchservice,
    aws_emrserverless as emrserverless
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
                      attribute_name="AlertId", 
                      #hash -- partition key - RANGE - sort key
                      key_type="HASH"
            )],

                # the properties below are optional
            attribute_definitions=[dynamodb.CfnTable.AttributeDefinitionProperty(
            # The data type for the attribute, where:. - S - the attribute is of type String - N - the attribute is of type Number - B - the attribute is of type Binary
                attribute_name="AlertId",
                attribute_type="S"
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
        

        opensearchservice.CfnDomain(self, "MyCfnDomain",
                 domain_name="fusion1",
                 engine_version="OpenSearch_1.1",
                 cluster_config=opensearchservice.CfnDomain.ClusterConfigProperty(
                     dedicated_master_count=3,
                     dedicated_master_enabled=True,
                     dedicated_master_type="r6g.large.search",
                     instance_count=3,
                     instance_type="r6g.large.search",
                    #  warm_count=3,
                    #  warm_enabled=False,
                    #  warm_type="r6g.large.search",
                    #  zone_awareness_config=opensearchservice.CfnDomain.ZoneAwarenessConfigProperty(
                    #     availability_zone_count=3
                    #  ),
                     zone_awareness_enabled=False
                ),
                ebs_options=opensearchservice.CfnDomain.EBSOptionsProperty(
                     ebs_enabled=True,
                     iops=3000,
                     throughput=125,
                     volume_size=50,
                     volume_type="gp3"
                ),
                tags= [{'key': 'environment', 'value': 'development'}],

            )
            

        emrserverless.CfnApplication(self, "MyCfnApplication",
                release_label="emr-6.9.0",
                name="fusion-subscriber",
                type="Spark",
                auto_start_configuration=emrserverless.CfnApplication.AutoStartConfigurationProperty(
                        enabled=True
                    ),
                auto_stop_configuration=emrserverless.CfnApplication.AutoStopConfigurationProperty(
                        enabled=True,
                        idle_timeout_minutes=100
                    ),
                initial_capacity=[emrserverless.CfnApplication.InitialCapacityConfigKeyValuePairProperty(
                    key="Executor",
                    value=emrserverless.CfnApplication.InitialCapacityConfigProperty(
                        worker_configuration=emrserverless.CfnApplication.WorkerConfigurationProperty(
                            cpu="4 vCPU",
                            memory="16 GB",
                            disk="20 GB"
                        ),
                        worker_count=3
                    )
                 ),
                 emrserverless.CfnApplication.InitialCapacityConfigKeyValuePairProperty(
                    key="Driver",
                    value=emrserverless.CfnApplication.InitialCapacityConfigProperty(
                        worker_configuration=emrserverless.CfnApplication.WorkerConfigurationProperty(
                            cpu="4 vCPU",
                            memory="16 GB",
                            disk="20 GB"
                        ),
                        worker_count=1
                    )
                 )],
                 
                 
                maximum_capacity=emrserverless.CfnApplication.MaximumAllowedResourcesProperty(
                        cpu="400 vCPU",
                        memory="3000 GB",

                        # the properties below are optional
                        disk="20000 GB"
                    ),


                 tags= [{'key': 'environment', 'value': 'development'}],      
                

            )



