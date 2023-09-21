from azure.ai.ml import MLClient
from azure.ai.ml import command

import azml_config as cfg
import az_utils as utils

utils.log("INFO: Getting credentials")
credential = utils.get_az_credentials()

#INITIALIZE AZ ML CLIENT
utils.log("INFO: Initializing AzML Client")
ml_client = MLClient(credential, cfg.az_subscription_id, cfg.az_resource_group, cfg.az_ml_workspace_name)

custom_environments  = ml_client.environments.list(name=cfg.az_ml_environment_name)
environment_versions = [environment.version for environment in custom_environments]

utils.log("INFO: Creating a job for model training")
job = command(
    code=cfg.az_ml_job_folder,
    command="python {}".format(cfg.az_ml_job_script),
    environment="{}:{}".format(cfg.az_ml_environment_name, environment_versions[-1]),
    compute=cfg.az_ml_compute_cluster,
    display_name="model_training",
    experiment_name="model_training"
)

returned_job = ml_client.create_or_update(job)

utils.log("INFO: Monitor your job at {}".format(returned_job.studio_url))

print(ml_client.jobs.list())