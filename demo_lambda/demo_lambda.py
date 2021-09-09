from aws_cdk import (core,
                     aws_apigateway as apigateway,
                     aws_s3 as s3,
                     aws_lambda as lambda_,
                     aws_dynamodb as dynamodb,
                     aws_iam as iam)


class DemoLambdaService(core.Stack):
    def __init__(self, scope: core.Construct, id: str):
        super().__init__(scope, id)

        # API Root
        api = apigateway.RestApi(self, "DemoLambdaApi",
            rest_api_name="Demo Lambda Service",
            description="This service allows you to add and fetch items from dynamodb.")

        items = api.root.add_resource("items")

        # Dynamo DB table
        table = dynamodb.Table(self, "DemoDynamoTable",
            partition_key=dynamodb.Attribute(name="pk", type=dynamodb.AttributeType.STRING),
            removal_policy=core.RemovalPolicy.DESTROY,
            sort_key=dynamodb.Attribute(name="name", type=dynamodb.AttributeType.STRING),
        )

        # Get All handler
        get_all_handler = lambda_.Function(self, "GetAllDemoLambdaHandler",
            runtime=lambda_.Runtime.NODEJS_14_X,
            code=lambda_.Code.from_asset("demo_lambda_resources/items_api"),
            handler="app.getAllItemsHandler",
            environment=dict(
                TABLE_NAME=table.table_name
            )
        )

        get_all_handler.add_to_role_policy(
            iam.PolicyStatement(
                actions=["dynamodb:*"],
                resources=[table.table_arn]
            )
        )
        get_items_integration = apigateway.LambdaIntegration(get_all_handler)
        items.add_method("GET", get_items_integration)

        # Post item handler
        post_item_handler = lambda_.Function(self, "PostDemoLambdaHandler",
            runtime=lambda_.Runtime.NODEJS_14_X,
            code=lambda_.Code.from_asset("demo_lambda_resources/items_api"),
            handler="app.addItemHandler",
            environment=dict(
                TABLE_NAME=table.table_name
            )
        )

        post_item_handler.add_to_role_policy(
            iam.PolicyStatement(
                actions=["dynamodb:*"],
                resources=[table.table_arn]
            )
        )
        post_items_integration = apigateway.LambdaIntegration(post_item_handler)
        items.add_method("POST", post_items_integration)
