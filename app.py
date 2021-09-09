import os

from aws_cdk import core as cdk
from aws_cdk import core
from demo_lambda.demo_lambda import DemoLambdaService

app = core.App()
DemoLambdaService(
    app,
    "edgarDemoLambdaService"
)
app.synth()