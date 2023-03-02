
from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_opensearchservice as opensearchservice,
    aws_emrserverless as emrserverless,
    aws_scheduler as scheduler,
     aws_iam as iam
    # core
)
from constructs import Construct

class FusionSubscriberStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        
        # s3.CfnBucket( self, "fusion-bucket-1",bucket_name="fusion-bucket-2",
        #                 access_control="Private", 
        #                 bucket_encryption=s3.CfnBucket.BucketEncryptionProperty( 
        #                     server_side_encryption_configuration=[ 
        #                         s3.CfnBucket.ServerSideEncryptionRuleProperty( 
        #                             server_side_encryption_by_default=s3.CfnBucket.ServerSideEncryptionByDefaultProperty( 
        #                                 sse_algorithm="AES256" ) ) ] ), 
        #                 public_access_block_configuration=s3.BlockPublicAccess.BLOCK_ALL,
        #                 tags= [{'key': 'environment', 'value': 'development'}, {'key': 'component', 'value': 'subscriber'}],
        #                 versioning_configuration=s3.CfnBucket.VersioningConfigurationProperty(status="Enabled"))
# custom role policy        
        # AmazonEventBridgeSchedulerExecutionPolicytrust_policy = {
        #     "Version": "2012-10-17",
        #     "Statement": [{
        #         "Effect": "Allow",
        #         "Principal": {"Service": "scheduler.amazonaws.com"},
        #         "Action":  ["sts:AssumeRole"],
        #         # "Condition":  {"StringEquals": {
        #         #     "aws:SourceArn": "arn:aws:scheduler:us-east-2:276301730779:schedule/default/testschedule",
        #         #     "aws:SourceAccount": "276301730779"
        #         #   }
        #            }
        #           ]
        #          }
        
        # AmazonEventBridgeSchedulerExecutionPolicy = {
        #     "Version": "2012-10-17",
        #     "Statement": [{
        #         # "Sid": "Amazon-EventBridge-Scheduler-Execution-Policy",
        #         "Effect": "Allow",
        #         "Action":  ["lambda:InvokeFunction"],
        #         "Resource": ["*"]
        #     }
        #     ]
        # }


        
        # custom_policy_document = iam.PolicyDocument.from_json(policy_document)
        # iam.Policy(self, "Amazon-EventBridge-Scheduler-Execution-Policy",document=custom_policy_document)

# # create role    
#         role= iam.Role(self, "Amazon_EventBridge_Scheduler_LAMBDA_cdk",
#                     assumed_by=iam.ServicePrincipal("scheduler.amazonaws.com")
#                 )
#  # for default policy
#         role.add_to_policy(iam.PolicyStatement(
#                     resources=["arn:aws:lambda:us-east-2:276301730779:function:test:", "arn:aws:lambda:us-east-2:276301730779:function:test"],
#                     actions=["lambda:InvokeFunction"],

#                 ))
        

        # iam.CfnRole(self, "MyCfnRole",
        #     assume_role_policy_document=AmazonEventBridgeSchedulerExecutionPolicytrust_policy,

        #     # the properties below are optional
        #     description="Amazon_EventBridge_Scheduler_LAMBDA using cfnRole",
        #     # managed_policy_arns=["managedPolicyArns"],
        #     # max_session_duration=123,
        #     # path="path",
        #     # permissions_boundary="permissionsBoundary",
        #     policies=[iam.CfnRole.PolicyProperty(
        #         policy_document=AmazonEventBridgeSchedulerExecutionPolicy,
        #         policy_name="Amazon-EventBridge-Scheduler-Execution-Policy"
        #     )],
        #     role_name="Amazon_EventBridge_Scheduler_LAMBDA_cfnRole",
        #     tags= [{'key': 'environment', 'value': 'development'}],
        # )

        service_role = self.create_service_role()


        scheduler.CfnSchedule(self, "MyCfnSchedule",
                flexible_time_window=scheduler.CfnSchedule.FlexibleTimeWindowProperty(
                    mode="OFF",

                    # the properties below are optional
                    # maximum_window_in_minutes=13
                ),
                schedule_expression="cron(0/3 * * * ? *)",
                target=scheduler.CfnSchedule.TargetProperty(
                    arn="arn:aws:lambda:us-east-2:276301730779:function:test",
                    role_arn=service_role.role_arn,

                    # the properties below are optional
                    # dead_letter_config=scheduler.CfnSchedule.DeadLetterConfigProperty(
                    #     arn="arn"
                    ),
                    # ecs_parameters=scheduler.CfnSchedule.EcsParametersProperty(
                    #     task_definition_arn="taskDefinitionArn",

                    #     # the properties below are optional
                    #     capacity_provider_strategy=[scheduler.CfnSchedule.CapacityProviderStrategyItemProperty(
                    #         capacity_provider="capacityProvider",

                    #         # the properties below are optional
                    #         base=123,
                    #         weight=123
                    #     )],
                    #     enable_ecs_managed_tags=False,
                    #     enable_execute_command=False,
                    #     group="group",
                    #     launch_type="launchType",
                    #     network_configuration=scheduler.CfnSchedule.NetworkConfigurationProperty(
                    #         awsvpc_configuration=scheduler.CfnSchedule.AwsVpcConfigurationProperty(
                    #             subnets=["subnets"],

                    #             # the properties below are optional
                    #             assign_public_ip="assignPublicIp",
                    #             security_groups=["securityGroups"]
                    #         )
                    #     ),
                    #     placement_constraints=[scheduler.CfnSchedule.PlacementConstraintProperty(
                    #         expression="expression",
                    #         type="type"
                    #     )],
                    #     placement_strategy=[scheduler.CfnSchedule.PlacementStrategyProperty(
                    #         field="field",
                    #         type="type"
                    #     )],
                    #     platform_version="platformVersion",
                    #     propagate_tags="propagateTags",
                    #     reference_id="referenceId",
                    #     # tags=tags,
                    #     task_count=123
                    # ),
                    # event_bridge_parameters=scheduler.CfnSchedule.EventBridgeParametersProperty(
                    #     detail_type="detailType",
                    #     source="source"
                    # ),
                    # input="input",
                    # kinesis_parameters=scheduler.CfnSchedule.KinesisParametersProperty(
                    #     partition_key="partitionKey"
                    # ),
                    # retry_policy=scheduler.CfnSchedule.RetryPolicyProperty(
                    #     maximum_event_age_in_seconds=123,
                    #     maximum_retry_attempts=123
                    # ),
                    # sage_maker_pipeline_parameters=scheduler.CfnSchedule.SageMakerPipelineParametersProperty(
                    #     pipeline_parameter_list=[scheduler.CfnSchedule.SageMakerPipelineParameterProperty(
                    #         name="name",
                    #         value="value"
                    #     )]
                    # ),
                    # sqs_parameters=scheduler.CfnSchedule.SqsParametersProperty(
                    #     message_group_id="messageGroupId"
                    # )

                )
        


    def create_service_role(self) -> iam.Role:
            return iam.Role(
                self,
                "eventschedulerServiceRole",
                assumed_by=iam.ServicePrincipal("scheduler.amazonaws.com"),
                managed_policies=[
                    iam.ManagedPolicy(
                        self,
                        "eventschedulerServiceRolePolicy",
                        statements=[
                            iam.PolicyStatement(
                                # sid="Amazon-EventBridge-Scheduler-Execution-Policy",
                                actions=[
                                    "lambda:InvokeFunction"
                                ],
                                resources=["*"],
                            ),
                            
                        ],
                    )
                ],
            )


        
            
             
                




