from azure.ai.ml import MLClient
from azure.ai.ml import command, Input
from azure.ai.ml.sweep import Choice, Uniform, MedianStoppingPolicy
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import ModelType

import azml_config as cfg
import az_utils as utils

utils.log("INFO: Getting credentials")
credential = utils.get_az_credentials()

#INITIALIZE AZ ML CLIENT
utils.log("INFO: Initializing AzML Client")
ml_client = MLClient(credential, cfg.az_subscription_id, cfg.az_resource_group, cfg.az_ml_workspace_name)

job = ml_client.jobs.get(cfg.az_ml_job_name)
best_run_id = job.properties['best_child_run_id']

best_model = Model(
    path="runs:/{}/model/".format(best_run_id),
    name=cfg.az_ml_model_name,
    description="Model created from run.",
    type='mlflow_model'
)

ml_client.models.create_or_update(best_model) 