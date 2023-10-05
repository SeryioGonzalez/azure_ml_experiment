from azure.ai.ml import MLClient
from azure.ai.ml import command, Input
from azure.ai.ml.sweep import Choice, Uniform, MedianStoppingPolicy

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
command_job = command(
    code=cfg.az_ml_job_folder,
    command="python main.py --iris-csv ${{inputs.iris_csv}} --learning-rate ${{inputs.learning_rate}} --boosting ${{inputs.boosting}}",
    environment="{}:{}".format(cfg.az_ml_environment_name, environment_versions[-1]),
    compute=cfg.az_ml_compute_cluster,
    display_name=cfg.az_ml_job_name,
    experiment_name=cfg.az_ml_job_name,
    inputs={
        "iris_csv": Input(
            type="uri_file",
            path="https://azuremlexamples.blob.core.windows.net/datasets/iris.csv",
<<<<<<< HEAD
        ), 
=======
        ),
>>>>>>> 0fe29b3c7329db5b810db9740c0a79a4d5dd5c1f
        "learning_rate": 0.9,
        "boosting": "gbdt"
    }
)

# Override your inputs with parameter expressions
command_job_for_sweep = command_job(
    learning_rate=Uniform(min_value=0.01, max_value=0.9),
    boosting=Choice(values=["gbdt", "dart"]),
)

# Call sweep() on your command job to sweep over your parameter expressions
sweep_job = command_job_for_sweep.sweep(
    compute=cfg.az_ml_compute_cluster,
    sampling_algorithm="random",
    primary_metric="test-multi_logloss",
    goal="Minimize",
)

# Specify your experiment details
sweep_job.display_name    = cfg.az_ml_job_name
sweep_job.name            = cfg.az_ml_job_name
sweep_job.experiment_name = cfg.az_ml_job_name
sweep_job.description     = cfg.az_ml_job_name

# Define the limits for this sweep
sweep_job.set_limits(max_total_trials=20, max_concurrent_trials=10, timeout=7200)

# Set early stopping on this one
sweep_job.early_termination = MedianStoppingPolicy(
    delay_evaluation=5, evaluation_interval=2
)

# submit the sweep
returned_sweep_job = ml_client.create_or_update(sweep_job)
