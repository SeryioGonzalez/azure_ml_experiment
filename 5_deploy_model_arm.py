from azure.ai.ml import MLClient
from azure.ai.ml.entities import Model, ManagedOnlineDeployment
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode

import json
import sys

import azml_config as cfg
import az_utils as utils

utils.log("INFO: Getting credentials")
credential = utils.get_az_credentials()

#INITIALIZE AZ ML CLIENT
utils.log("INFO: Initializing AzML Client")
ml_client = MLClient(credential, cfg.az_subscription_id, cfg.az_resource_group, cfg.az_ml_workspace_name)

utils.log("INFO: Listing AzML environments")
custom_environment = list(ml_client.environments.list(cfg.az_ml_environment_name))[0]

utils.log("INFO: Listing AzML models")
try:
    latest_model_version = max([int(m.version) for m in ml_client.models.list(name=cfg.az_ml_model_name)])
    model = ml_client.models.get(name=cfg.az_ml_model_name, version=latest_model_version)
except:
    utils.log("Model {} not found. Make sure AzML Job for model training has completed".format(cfg.az_ml_model_name))
    sys.exit()

utils.log("INFO: Creating online deployment")
with open("az_ml_online_deployment.json", "r") as template_file:
    template_body = json.load(template_file)

resource_client = ResourceManagementClient(credential, cfg.az_subscription_id)
rg_deployment_result = resource_client.deployments.begin_create_or_update(
    cfg.az_resource_group,
    "modelDeploymentOnline",
    {
        "properties": {
            "template": template_body,
            "parameters": {
                "endpointComputeType":  {"value": "Managed" },
                "environmentId":        {"value": custom_environment.id },
                "location":             {"value": cfg.az_region  },
                "model":                {"value": model.id },
                "onlineDeploymentName": {"value": cfg.az_ml_deployment_name },
                "onlineEndpointName":   {"value": cfg.az_ml_online_endpoint },
                "skuCapacity":          {"value": cfg.az_ml_initial_capacity },
                "skuName":              {"value": cfg.az_ml_inference_compute },
                "workspaceName":        {"value": cfg.az_ml_workspace_name }
            },
            "mode": DeploymentMode.incremental
        }
    }
)
