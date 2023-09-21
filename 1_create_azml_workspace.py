from azure.ai.ml import MLClient
from azure.ai.ml.entities import AmlCompute
from azure.ai.ml.entities import Workspace
from azure.mgmt.resource import ResourceManagementClient

import time

import azml_config as cfg
import az_utils as utils

utils.log("INFO: Getting credentials")
credential = utils.get_az_credentials()

#CHECK RG IS CREATED
utils.log("INFO: Checking RG {} exists. If not creating it".format(cfg.az_resource_group ))
resource_client = ResourceManagementClient(credential, cfg.az_subscription_id)
rg_result = resource_client.resource_groups.create_or_update(cfg.az_resource_group, {"location": cfg.az_region})

while [rg.properties.provisioning_state for rg in resource_client.resource_groups.list() if rg.name == cfg.az_resource_group][0] != 'Succeeded':
    utils.log("INFO: Waiting for RG {} to be created".format(cfg.az_resource_group))
    time.sleep(5)

#INITIALIZE AZ ML CLIENT
utils.log("INFO: Initializing AzML Client")
ml_client = MLClient(credential, cfg.az_subscription_id, cfg.az_resource_group, cfg.az_ml_workspace_name)

ws_basic = Workspace(
    name=cfg.az_ml_workspace_name,
    location=cfg.az_region,
)

utils.log("INFO: Initializing AzML workspace")
workspace = ml_client.workspaces.begin_create(ws_basic)

workspace_created = False

while workspace_created is False:
    try:
        created_workspace = ml_client.workspaces.get(cfg.az_ml_workspace_name)
        workspace_created = True
    except:
        utils.log("INFO: Waiting for AzML workspace creation")
        time.sleep(5)
        continue

utils.log("INFO: AzML workspace {} created".format(cfg.az_ml_workspace_name))

utils.log("INFO: Initializing AzML compute cluster")
try:
    # let's see if the compute target already exists
    compute_cluster = ml_client.compute.get(cfg.az_ml_compute_cluster)
    utils.log("INFO You already have an AzML compute named {}, we'll reuse it as is.".format(cfg.az_ml_compute_cluster))

except Exception:
    utils.log("INFO: Creating a new AzML compute cluster...")

    # Let's create the Azure ML compute object with the intended parameters
    compute_cluster_config = AmlCompute(
        name=cfg.az_ml_compute_cluster,
        type="amlcompute",
        size=cfg.az_ml_compute_instance_size,
        # Minimum running nodes when there is no job running
        min_instances=0,
        # Nodes in cluster
        max_instances=cfg.az_ml_max_compute_instances,
        # How many seconds will the node running after the job termination
        idle_time_before_scale_down=120,
        # Dedicated or LowPriority. The latter is cheaper but there is a chance of job termination
        tier="Dedicated",
    )

    # Now, we pass the object to MLClient's create_or_update method
    compute_cluster = ml_client.compute.begin_create_or_update(compute_cluster_config)
    
    while not compute_cluster.done() :
        utils.log("INFO: Waiting for AzML compute cluster to be ready")
        time.sleep(3)

utils.log("INFO: AzML compute cluster {} available".format(cfg.az_ml_compute_cluster))