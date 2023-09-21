from azure.ai.ml import MLClient
from azure.ai.ml.entities import ManagedOnlineEndpoint

import azml_config as cfg
import az_utils as utils

utils.log("INFO: Getting credentials")
credential = utils.get_az_credentials()

#INITIALIZE AZ ML CLIENT
utils.log("INFO: Initializing AzML Client")
ml_client = MLClient(credential, cfg.az_subscription_id, cfg.az_resource_group, cfg.az_ml_workspace_name)

utils.log("INFO: Creating online endpoint")
endpoint = ManagedOnlineEndpoint(
    name=cfg.az_ml_online_endpoint,
    description="Online endpoint for MLflow diabetes model",
    auth_mode="key",
)

ml_client.online_endpoints.begin_create_or_update(endpoint).result()