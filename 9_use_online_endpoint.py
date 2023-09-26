from azure.ai.ml import MLClient
from azure.ai.ml.entities import Model, ManagedOnlineDeployment
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode

import ast
import json
import sys

import azml_config as cfg
import az_utils as utils

utils.log("INFO: Getting credentials")
credential = utils.get_az_credentials()

#INITIALIZE AZ ML CLIENT
utils.log("INFO: Initializing AzML Client")
ml_client = MLClient(credential, cfg.az_subscription_id, cfg.az_resource_group, cfg.az_ml_workspace_name)

utils.log("INFO: Sending a request")
# test the blue deployment with some sample data
responses = ml_client.online_endpoints.invoke(
    endpoint_name=cfg.az_ml_online_endpoint,
    deployment_name=cfg.az_ml_deployment_name,
    request_file="sample-data.json",
)

responses = ast.literal_eval(responses)[0]

classes = ["Setosa", "Versicolor", "Virginica"]

for index, value in enumerate(responses):
    print("Class {} as prob {}".format(classes[index], value))