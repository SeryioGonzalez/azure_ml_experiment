from azure.ai.ml import MLClient
from azure.ai.ml.entities import Environment, BuildContext

import azml_config as cfg
import az_utils as utils

utils.log("INFO: Getting credentials")
credential = utils.get_az_credentials()

#INITIALIZE AZ ML CLIENT
utils.log("INFO: Initializing AzML Client")
ml_client = MLClient(credential, cfg.az_subscription_id, cfg.az_resource_group, cfg.az_ml_workspace_name)

utils.log("INFO: Creating a custom environment with docker specs, since special packages are required")
custom_env = Environment(
    name=cfg.az_ml_environment_name,
    build=BuildContext(path="docker-context/")
)

custom_environment=ml_client.environments.create_or_update(custom_env)