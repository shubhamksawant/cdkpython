
from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_opensearchservice as opensearchservice,
    aws_emrserverless as emrserverless,
    aws_scheduler as scheduler,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_secretsmanager as secrets
    # core
)
from constructs import Construct
from aws_cdk import Tags
class FusionSubscriberStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        


        #  custom role policy        
        AmazonEventBridgeSchedulerExecutionPolicytrust_policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action":  ["sts:AssumeRole"],
                "Condition":  {"StringEquals": {
                    "aws:SourceArn": "arn:aws:scheduler:us-east-2:276301730779:schedule/default/testschedule",
                    "aws:SourceAccount": "276301730779"
                     }
                   }
                 }
                ]
            }
        
        
        AmazonEventBridgeSchedulerExecutionPolicy = {
            "Version": "2012-10-17",
            "Statement": [{
                # "Sid": "Amazon-EventBridge-Scheduler-Execution-Policy",
                "Effect": "Allow",
                "Action":  ["lambda:InvokeFunction"],
                "Resource": ["*"]
            },
            ]
        }

        AmazonEventBridgeSchedulerExecutionPolice = {
            "Version": "2012-10-17",
            "Statement": [{
                # "Sid": "Amazon-EventBridge-Scheduler-Execution-Policy",
                "Effect": "Allow",
                "Action":  ["lambda:InvokeFunction"],
                "Resource": ["*"]
            },
            {
                # "Sid": "Amazon-EventBridge-Scheduler-Execution-Policy",
                "Effect": "Allow",
                "Action":  ["lambda:GetFunction"],
                "Resource": ["*"]
            }
            ]
        }

        schedulerrole= iam.CfnRole(self, "MyCfnRole",
            assume_role_policy_document=AmazonEventBridgeSchedulerExecutionPolicytrust_policy,

            # the properties below are optional
            description="Amazon_EventBridge_Scheduler_LAMBDA using cfnRole",
            # managed_policy_arns=["managedPolicyArns"],
            # max_session_duration=123,
            # path="path",
            # permissions_boundary="permissionsBoundary",
            policies=[iam.CfnRole.PolicyProperty(
                policy_document=AmazonEventBridgeSchedulerExecutionPolicy,
                policy_name="Amazon-EventBridge-Scheduler-Execution-Policy",
            ), iam.CfnRole.PolicyProperty(
                policy_document=AmazonEventBridgeSchedulerExecutionPolice,
                policy_name="AmazonEventBridgeSchedulerExecutionPolice",
            )],
            role_name="Amazon_EventBridge_Scheduler_LAMBDA_cfnRole",
            tags= [{'key': 'environment', 'value': 'development'}],
        )
        
    


        
        # custom_policy_document = iam.PolicyDocument.from_json(policy_document)
        # iam.Policy(self, "Amazon-EventBridge-Scheduler-Execution-Policy",document=custom_policy_document)

# # create role    
#         role= iam.Role(self, "ServerlessEMRJobRole",
#                     assumed_by=iam.ServicePrincipal("emr-serverless.amazonaws.com"),

#                 )
#   # for aws manage policies       
#         AmazonS3FullAccess = iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
#         role.add_managed_policy(AmazonS3FullAccess)

#         AmazonDynamoDBFullAccess = iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess')
#         role.add_managed_policy(AmazonDynamoDBFullAccess)

#  # for default policyy
#         role.add_to_policy(iam.PolicyStatement(
#                     resources=["arn:aws:lambda:us-east-2:276301730779:function:test:", "arn:aws:lambda:us-east-2:276301730779:function:test"],
#                     actions=["lambda:InvokeFunction"],

#                 ))
        
#         role.attach_inline_policy(iam.Policy(self, "Glue-Full-Access", statements=[iam.PolicyStatement(
#         actions=["glue:*"],
#         resources=["*"],
#         effect= iam.Effect.ALLOW,
#     )]
# ))
        # my_custom_policy = iam.PolicyDocument(
        #     statements=[iam.PolicyStatement(
        #         actions=["kms:Create*", "kms:Describe*", "kms:Enable*", "kms:List*", "kms:Put*"],               ffffffffff
        #         principals=[iam.AccountRootPrincipal()],
        #         resources=["*"]
        #     )]
        # )
        
        # lambda_role = iam.Role(self, "Role",
        #                 assumed_by= iam.add_to_policy(
        #             iam.PolicyStatement( # Restrict to listing and describing tables
        #             principals=[iam.AnyPrincipal()],
        #             actions=["dynamodb:DescribeTable", "dynamodb:ListTables"],
        #             resources=["*"]))
        #     # iam.add_to_principal_policy(AmazonEventBridgeSchedulerExecutionPolicytrust_policy),
        #     # ServicePrincipal("lambda.amazonaws.com"),
        #     description="Example role...",
        #     # inline_policies= addToPolicy 

        # )
        
        
        # alertbucket= s3.Bucket(self, "fusion-bucket-1",
        #                   bucket_name="fusion-bucket-2",
        #                   block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        #                   bucket_key_enabled= False , encryption= s3.BucketEncryption.S3_MANAGED,
        #                   versioned= True,
        #                 #   RemovalPolicy=s3.RemovalPolicy.DESTROY                                     
                          
        #                   )
        
        # Tags.of(alertbucket).add("key1", "value1")
        # Tags.of(alertbucket).add("key2", "value2")


        # alertdynaomodb = dynamodb.Table(self, "MyCfnTable",
        #                 table_name= "fusiondynamodbtable",
        #                 encryption= dynamodb.TableEncryption.AWS_MANAGED,
        #                 partition_key=dynamodb.Attribute(name="ref_event_uid", type=dynamodb.AttributeType.STRING),
        #         #     replication_regions=["us-east-1", "us-east-2", "us-west-2"],
        #                 billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        #                 table_class=dynamodb.TableClass.STANDARD

        #          )
        

        # emr = emrserverless.CfnApplication(self, "MyCfnApplication",
        #         release_label="emr-6.9.0",
        #         name="fusion-subscriber",
        #         type="Spark",
        #         auto_start_configuration=emrserverless.CfnApplication.AutoStartConfigurationProperty(
        #                 enabled=True
        #             ),
        #         auto_stop_configuration=emrserverless.CfnApplication.AutoStopConfigurationProperty(
        #                 enabled=True,
        #                 idle_timeout_minutes=100
        #             ),
        #         initial_capacity=[emrserverless.CfnApplication.InitialCapacityConfigKeyValuePairProperty(
        #             key="Executor",
        #             value=emrserverless.CfnApplication.InitialCapacityConfigProperty(
        #                 worker_configuration=emrserverless.CfnApplication.WorkerConfigurationProperty(
        #                     cpu="4 vCPU",
        #                     memory="16 GB",
        #                     disk="20 GB"
        #                 ),
        #                 worker_count=3
        #             )
        #          ),
        #          emrserverless.CfnApplication.InitialCapacityConfigKeyValuePairProperty(
        #             key="Driver",
        #             value=emrserverless.CfnApplication.InitialCapacityConfigProperty(
        #                 worker_configuration=emrserverless.CfnApplication.WorkerConfigurationProperty(
        #                     cpu="4 vCPU",
        #                     memory="16 GB",
        #                     disk="20 GB"
        #                 ),
        #                 worker_count=1
        #             )
        #          )],
                 
                 
        #         maximum_capacity=emrserverless.CfnApplication.MaximumAllowedResourcesProperty(
        #                 cpu="400 vCPU",
        #                 memory="3000 GB",

        #                 # the properties below are optional
        #                 disk="20000 GB"
        #             ),


        #          tags= [{'key': 'environment', 'value': 'development'}],      
                

        #     )



    #     self.build_lambda_func()

    # def build_lambda_func(self):
    #     secret_name = "secretsExample"
    #     self.secrets_lambda = _lambda.Function(
    #         scope=self,
    #         id="LambdaWithSecrets",
    #         runtime=_lambda.Runtime.PYTHON_3_9,
    #         function_name="LambdaWithSecretsExample",
    #         code=_lambda.Code.from_asset(
    #             path="lambda"
    #         ),
    #         handler="lambda_with_secrets.handler",
    #         # We need these env vars to access the secret inside the lambda
    #         environment={
    #             "secret_name": secret_name,
    #             "secret_region": os.environ["CDK_DEFAULT_REGION"],
    #         },
    #     )
    #     # Grant permission to the Lambda func to access the secret
    #     example_secret = secrets.Secret.from_secret_name_v2(
    #         scope=self, id="secretExample", secret_name=secret_name
    #     )
    #     example_secret.grant_read(grantee=self.secrets_lambda)




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

# create role    
        # role= iam.Role(self, "Invoke-Serverless-EMR-Job-role-269yf7a8",
        #             assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),

        #         )
        
#         role.attach_inline_policy(iam.Policy(self, "PassRole_For_Lambda", statements=[iam.PolicyStatement(
#         # sid = ["VisualEditor0"],
#         actions=["iam:PassRole"],
#         resources=["*"],
#         effect= iam.Effect.ALLOW,
#     )]
# ))
        



        service_rolelambda = self.create_service_rolelambda()

        # # my_custom_policy = iam.PolicyDocument(
        # #     statements=[iam.PolicyStatement(
        # #         actions=["kms:Create*", "kms:Describe*", "kms:Enable*", "kms:List*", "kms:Put*"], 
        # #         principals=[iam.AccountRootPrincipal()],
        # #         resources=["*"]
        # #     )]
        # # )
        
        # # service_rolelambda.add_to_policy(statements=[iam.PolicyStatement(
        # #         actions=["kms:Create*", "kms:Describe*", "kms:Enable*", "kms:List*", "kms:Put*"], 
        # #         principals=[iam.AccountRootPrincipal()],
        # #         resources=["*"]
        # #     )])

        my_policyemr = iam.PolicyStatement(
                    # sid= ["VisualEditor1"],
                    effect=iam.Effect.ALLOW,
                    actions=[
                       "elasticmapreduce:DescribeNotebookExecution",
                "emr-serverless:GetDashboardForJobRun",
                "elasticmapreduce:ListBootstrapActions",
                "elasticmapreduce:GetOnClusterAppUIPresignedURL",
                "elasticmapreduce:RemoveAutoTerminationPolicy",
                "elasticmapreduce:CreateEditor",
                "elasticmapreduce:CreateSecurityConfiguration",
                "elasticmapreduce:LinkRepository",
                "elasticmapreduce:GetClusterSessionCredentials",
                "elasticmapreduce:SetTerminationProtection",
                "elasticmapreduce:StopNotebookExecution",
                "elasticmapreduce:ListRepositories",
                "elasticmapreduce:ListInstanceGroups",
                "elasticmapreduce:AttachEditor",
                "emr-serverless:UpdateApplication",
                "elasticmapreduce:ListInstances",
                "elasticmapreduce:RemoveManagedScalingPolicy",
                "elasticmapreduce:ListSecurityConfigurations",
                "elasticmapreduce:DescribePersistentAppUI",
                "elasticmapreduce:CreateStudio",
                "elasticmapreduce:DescribeSecurityConfiguration",
                "elasticmapreduce:PutManagedScalingPolicy",
                "elasticmapreduce:DescribeReleaseLabel",
                "emr-serverless:StopApplication",
                "elasticmapreduce:ViewEventsFromAllClustersInConsole",
                "elasticmapreduce:DescribeRepository",
                "elasticmapreduce:ListSteps",
                "emr-serverless:GetJobRun",
                "elasticmapreduce:GetStudioSessionMapping",
                "elasticmapreduce:ListNotebookExecutions",
                "elasticmapreduce:CreateStudioSessionMapping",
                "emr-serverless:CancelJobRun",
                "elasticmapreduce:ModifyInstanceFleet",
                "elasticmapreduce:CreateRepository",
                "elasticmapreduce:StartEditor",
                "elasticmapreduce:RemoveAutoScalingPolicy",
                "elasticmapreduce:AddInstanceFleet",
                "elasticmapreduce:UnlinkRepository",
                "elasticmapreduce:ListStudios",
                "elasticmapreduce:CancelSteps",
                "elasticmapreduce:GetManagedScalingPolicy",
                "elasticmapreduce:GetBlockPublicAccessConfiguration",
                "emr-serverless:ListTagsForResource",
                "elasticmapreduce:UpdateStudioSessionMapping",
                "elasticmapreduce:DescribeStudio",
                "emr-serverless:ListApplications",
                "elasticmapreduce:DescribeCluster",
                "emr-serverless:StartApplication",
                "elasticmapreduce:GetPersistentAppUIPresignedURL",
                "elasticmapreduce:DescribeStep",
                "emr-serverless:CreateApplication",
                "elasticmapreduce:CreateStudioPresignedUrl",
                "elasticmapreduce:DetachEditor",
                "elasticmapreduce:CreatePersistentAppUI",
                "emr-serverless:GetApplication",
                "elasticmapreduce:StopEditor",
                "elasticmapreduce:DescribeEditor",
                "elasticmapreduce:ListClusters",
                "elasticmapreduce:GetAutoTerminationPolicy",
                "emr-serverless:ListJobRuns",
                "elasticmapreduce:UpdateStudio",
                "elasticmapreduce:OpenEditorInConsole",
                "elasticmapreduce:ListInstanceFleets",
                "elasticmapreduce:PutAutoScalingPolicy",
                "elasticmapreduce:ModifyCluster",
                "elasticmapreduce:UpdateEditor",
                "elasticmapreduce:PutAutoTerminationPolicy",
                "elasticmapreduce:AddInstanceGroups",
                "elasticmapreduce:ListReleaseLabels",
                "elasticmapreduce:UpdateRepository",
                "elasticmapreduce:StartNotebookExecution",
                "elasticmapreduce:ModifyInstanceGroups",
                "emr-serverless:StartJobRun",
                "elasticmapreduce:RunJobFlow",
                "elasticmapreduce:ListWorkspaceAccessIdentities",
                "elasticmapreduce:AddJobFlowSteps",
                "elasticmapreduce:ListEditors",
                "elasticmapreduce:DescribeJobFlows",
                "elasticmapreduce:ListStudioSessionMappings"
                    ],
                    resources=["*"]
                )

        service_rolelambda.add_to_policy(my_policyemr)

        service_rolelambda.attach_inline_policy(iam.Policy(self, "AWSLambdaBasicExecutionRole", statements=[iam.PolicyStatement(
                # sid = ["VisualEditor0"],
                actions= ["logs:CreateLogGroup"],
                resources=["*"],
                effect= iam.Effect.ALLOW,
            ),
            iam.PolicyStatement(
                # sid = ["VisualEditor0"],
                actions= [ "logs:CreateLogStream",
                "logs:PutLogEvents"],
                resources=["*"],
                effect= iam.Effect.ALLOW,
            ),
            iam.PolicyStatement(
                # sid = ["VisualEditor0"],
                actions= [  "emr-serverless:CreateApplication",
                "emr-serverless:UpdateApplication",
                "emr-serverless:ListApplications",
                "emr-serverless:GetApplication",
                "emr-serverless:StartApplication",
                "emr-serverless:StopApplication",
                "emr-serverless:StartJobRun",
                "emr-serverless:CancelJobRun",
                "emr-serverless:ListJobRuns",
                "emr-serverless:GetJobRun"],
                resources=["*"],
                effect= iam.Effect.ALLOW,
            ),
            ]
        ))

        my_policy1 = iam.PolicyStatement(
                    # sid= ["VisualEditor1"],
                    effect=iam.Effect.ALLOW,
                    actions=[
                       "emr-serverless:CreateApplication",
                        "emr-serverless:UpdateApplication",
                        "emr-serverless:ListApplications",
                        "emr-serverless:GetApplication",
                        "emr-serverless:StartApplication",
                        "emr-serverless:StopApplication",
                        "emr-serverless:StartJobRun",
                        "emr-serverless:CancelJobRun",
                        "emr-serverless:ListJobRuns",
                        "emr-serverless:GetJobRun"
                    ],
                    resources=["*"]
                )
        
        service_rolelambda.add_to_policy(my_policy1)    

        my_policy2 = iam.PolicyStatement(
                    # sid= ["VisualEditor1"],
                    effect=iam.Effect.ALLOW,
                    actions=[
                       "logs:CreateLogStream",
                       "logs:PutLogEvents"
                    ],
                    resources=["*"]
                )
        service_rolelambda.add_to_policy(my_policy2)  

        my_policy3 = iam.PolicyStatement(
                    # sid= ["VisualEditor1"],
                    effect=iam.Effect.ALLOW,
                    actions=[
                       "logs:CreateLogGroup"
                    ],
                    resources=["*"]
                )
               
        service_rolelambda.add_to_policy(my_policy3)
      

        # policy_doc = iam.PolicyDocument(
        #     statements=[
        #         iam.PolicyStatement(
        #             effect=iam.Effect.ALLOW,
        #             actions=[
        #                 "emr-serverless:CreateApplication",
        #                 "emr-serverless:UpdateApplication",
        #                 "emr-serverless:ListApplications",
        #                 "emr-serverless:GetApplication",
        #                 "emr-serverless:StartApplication",
        #                 "emr-serverless:StopApplication",
        #                 "emr-serverless:StartJobRun",
        #                 "emr-serverless:CancelJobRun",
        #                 "emr-serverless:ListJobRuns",
        #                 "emr-serverless:GetJobRun"],
        #             resources=["*"]
        #         ),
        #         iam.PolicyStatement(
        #             effect=iam.Effect.ALLOW,
        #             actions=["logs:CreateLogGroup"],
        #             resources=["*"]
        #         ),
        #         iam.PolicyStatement(
        #             effect=iam.Effect.ALLOW,
        #             actions=[
        #         "logs:CreateLogStream",
        #         "logs:PutLogEvents"
        #         ],
        #             resources=["*"]
        #         )
        #     ]
        # )

        # # Create the customer-managed policy
        # my_policy = iam.Policy(
        #     self,
        #     "MyPolicy",
        #     policy_name="MyCustomPolicy",
        #     document=policy_doc
        # )

        # # Create the IAM role and attach the policy
        # my_role = iam.Role(
        #     self,
        #     "MyRole",
        #     assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        #     role_name="MyCustomRole"
        # )
        # service_rolelambda.add_managed_policy(my_policy)
    







        service_role_emr = self.create_service_role_emr()

        #  for aws manage policies       
        AmazonS3FullAccess = iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
        service_role_emr.add_managed_policy(AmazonS3FullAccess)

        AmazonDynamoDBFullAccess = iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess')
        service_role_emr.add_managed_policy(AmazonDynamoDBFullAccess)

        my_lambda = _lambda.Function(
            self, 
            'FusionLambdaFunction',
            description='Deploying Lambda Function Infrastrcture',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            role= service_rolelambda,
            handler='hello.handler',
            environment={  
                        #    "bucket_name": alertbucket.bucket_name,
                            "exerole": service_role_emr.role_arn,
                            # "ddbtablename": alertdynaomodb.table_name,
                            # "application": emr.attr_application_id,
                            # "app_id": emr.logical_id

                    }
             )
            
             # Create a customer-managed policy and attach it to the Lambda function's role
        
        # my_lambda.role.attach_inline_policy(service_rolelambda)
        


    #     service_role_scheduler = self.create_service_role_scheduler()


    #     scheduler.CfnSchedule(self, "MyCfnSchedule",
    #             flexible_time_window=scheduler.CfnSchedule.FlexibleTimeWindowProperty(
    #                 mode="OFF",

    #                 # the properties below are optional
    #                 # maximum_window_in_minutes=13
    #             ),
    #             schedule_expression="cron(0/3 * * * ? *)",
    #             target=scheduler.CfnSchedule.TargetProperty(
    #                 arn=my_lambda.function_arn,
    #                 role_arn=service_role_scheduler.role_arn,

    #                 # the properties below are optional
    #                 # dead_letter_config=scheduler.CfnSchedule.DeadLetterConfigProperty(
    #                 #     arn="arn"
    #                 ),
    #                 # ecs_parameters=scheduler.CfnSchedule.EcsParametersProperty(
    #                 #     task_definition_arn="taskDefinitionArn",

    #                 #     # the properties below are optional
    #                 #     capacity_provider_strategy=[scheduler.CfnSchedule.CapacityProviderStrategyItemProperty(
    #                 #         capacity_provider="capacityProvider",

    #                 #         # the properties below are optional
    #                 #         base=123,
    #                 #         weight=123
    #                 #     )],
    #                 #     enable_ecs_managed_tags=False,
    #                 #     enable_execute_command=False,
    #                 #     group="group",
    #                 #     launch_type="launchType",
    #                 #     network_configuration=scheduler.CfnSchedule.NetworkConfigurationProperty(
    #                 #         awsvpc_configuration=scheduler.CfnSchedule.AwsVpcConfigurationProperty(
    #                 #             subnets=["subnets"],

    #                 #             # the properties below are optional
    #                 #             assign_public_ip="assignPublicIp",
    #                 #             security_groups=["securityGroups"]
    #                 #         )
    #                 #     ),
    #                 #     placement_constraints=[scheduler.CfnSchedule.PlacementConstraintProperty(
    #                 #         expression="expression",
    #                 #         type="type"
    #                 #     )],
    #                 #     placement_strategy=[scheduler.CfnSchedule.PlacementStrategyProperty(
    #                 #         field="field",
    #                 #         type="type"
    #                 #     )],
    #                 #     platform_version="platformVersion",
    #                 #     propagate_tags="propagateTags",
    #                 #     reference_id="referenceId",
    #                 #     # tags=tags,
    #                 #     task_count=123
    #                 # ),
    #                 # event_bridge_parameters=scheduler.CfnSchedule.EventBridgeParametersProperty(
    #                 #     detail_type="detailType",
    #                 #     source="source"
    #                 # ),
    #                 # input="input",
    #                 # kinesis_parameters=scheduler.CfnSchedule.KinesisParametersProperty(
    #                 #     partition_key="partitionKey"
    #                 # ),
    #                 # retry_policy=scheduler.CfnSchedule.RetryPolicyProperty(
    #                 #     maximum_event_age_in_seconds=123,
    #                 #     maximum_retry_attempts=123
    #                 # ),
    #                 # sage_maker_pipeline_parameters=scheduler.CfnSchedule.SageMakerPipelineParametersProperty(
    #                 #     pipeline_parameter_list=[scheduler.CfnSchedule.SageMakerPipelineParameterProperty(
    #                 #         name="name",
    #                 #         value="value"
    #                 #     )]
    #                 # ),
    #                 # sqs_parameters=scheduler.CfnSchedule.SqsParametersProperty(
    #                 #     message_group_id="messageGroupId"
    #                 # )

    #             )
        


    def create_service_rolelambda(self) -> iam.Role:
            return iam.Role(
                self,
                "Invoke-Serverless-EMR-Job-role",
                assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
                managed_policies=[
                    iam.ManagedPolicy(
                        self,
                        "PassRole_For_Lambda",
                        statements=[
                            iam.PolicyStatement(
                                sid="VisualEditor0",
                                actions=[
                                    "iam:GetRole",
                                     "iam:PassRole"
                                ],
                                resources=["*"],
                            ),

                            iam.PolicyStatement(
                                sid="VisualEditor1",
                                actions=[
                                     "iam:ListRoles"
                                ],
                                resources=["*"],
                            ),
                        ],
                        
                        
                    )
                ],
            )




    def create_service_role_emr(self) -> iam.Role:
            return iam.Role(
                self,
                "ServerlessEMRJobRole",
                assumed_by=iam.ServicePrincipal("emr-serverless.amazonaws.com"),
                managed_policies=[
                    iam.ManagedPolicy(
                        self,
                        "Glue-Full-Access",
                        statements=[
                            iam.PolicyStatement(
                                sid="VisualEditor0",
                                actions=[
                                    "glue:*"
                                ],
                                resources=["*"],
                            ),
                            
                        ],
                    )
                ],
            )

            
             
                




