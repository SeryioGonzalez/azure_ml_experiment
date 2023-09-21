from azure.ai.ml import MLClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.monitor.models import AutoscaleProfile, ScaleRule, MetricTrigger, ScaleAction

import datetime
import sys

import azml_config as cfg
import az_utils as utils

utils.log("INFO: Getting credentials")
credential = utils.get_az_credentials()

#INITIALIZE AZ ML CLIENT
utils.log("INFO: Initializing AzML Client")
ml_client = MLClient(credential, cfg.az_subscription_id, cfg.az_resource_group, cfg.az_ml_workspace_name)

utils.log("INFO: Initializing Monitor Client")
mon_client = MonitorManagementClient(credential,  cfg.az_subscription_id)

online_deployment_list = list(ml_client.online_deployments.list(endpoint_name=cfg.az_ml_online_endpoint))

if len(online_deployment_list) == 0:
    utils.log("ERROR: No deployents in endpoint {}".format(cfg.az_ml_online_endpoint))
    sys.exit()
else:
    model_deployment = online_deployment_list[0]

utils.log("INFO: Model in deployent is {}".format(model_deployment.model))

utils.log("INFO: Defining scale out rule")
rule_scale_out = ScaleRule(
    metric_trigger = MetricTrigger(
        metric_name=cfg.az_autoscale_settings_name,
        metric_resource_uri = model_deployment.id, 
        time_grain = datetime.timedelta(minutes = 1),
        statistic = "Average",
        operator = "GreaterThan", 
        time_aggregation = "Last",
        time_window = datetime.timedelta(minutes = 5), 
        threshold = cfg.az_ml_autoscale_scale_out_threashold
    ), 
    scale_action = ScaleAction(
        direction = "Increase", 
        type = "ChangeCount", 
        value = 2, 
        cooldown = datetime.timedelta(hours = 1)
    )
)

utils.log("INFO: Defining scale in rule")
rule_scale_in = ScaleRule(
    metric_trigger = MetricTrigger(
        metric_name=cfg.az_autoscale_settings_name,
        metric_resource_uri = model_deployment.id, 
        time_grain = datetime.timedelta(minutes = 1),
        statistic = "Average",
        operator = "LessThan", 
        time_aggregation = "Last",
        time_window = datetime.timedelta(minutes = 5), 
        threshold = cfg.az_ml_autoscale_scale_in_threashold
    ), 
    scale_action = ScaleAction(
        direction = "Decrease", 
        type = "ChangeCount", 
        value = 1, 
        cooldown = datetime.timedelta(hours = 1)
    )
)

utils.log("INFO: Creating autoscale rule")
mon_client.autoscale_settings.create_or_update(
    cfg.az_resource_group, 
    cfg.az_autoscale_settings_name, 
    parameters = {
        "location" : cfg.az_region,
        "enabled": True,
        "target_resource_uri" : model_deployment.id,
        "profiles" : [
            AutoscaleProfile(
                name="my-scale-settings",
                capacity={
                    "minimum" : 2, 
                    "maximum" : 5,
                    "default" : 2
                },
                rules = [
                    rule_scale_out, 
                    rule_scale_in
                ]
            )
        ]
    }
)