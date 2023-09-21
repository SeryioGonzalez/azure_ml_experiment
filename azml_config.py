import yaml

#GET CONFIGURATION
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

az_subscription_id          = cfg["azure"]["subscription_id"]
az_resource_group           = cfg["azure"]["resource_group"]
az_region                   = cfg["azureml"]["azure_region"]

az_ml_workspace_name   = "{}_workspace".format(az_resource_group)
az_ml_environment_name = "{}_environment".format(az_resource_group)
az_ml_compute_cluster  = "{}-compute".format(az_resource_group) 
az_ml_online_endpoint  = "{}-endpoint".format(az_resource_group) 
az_ml_deployment_name  = "{}-deployment".format(az_resource_group) 
az_ml_model_name       = "model"
az_autoscale_settings_name = "{}-autoscale_setting".format(az_resource_group) 

az_ml_compute_instance_size = cfg["azureml_job"]["compute_instance_size"] 
az_ml_max_compute_instances = cfg["azureml_job"]["compute_max_instances"] 

az_ml_job_folder            = cfg["azureml_job"]["training_folder"] 
az_ml_job_script            = cfg["azureml_job"]["training_script"] 
az_ml_job_name              = cfg["azureml_job"]["name"] 

az_ml_inference_compute = cfg["azureml_endpoint_autoscale_settings"]["compute_instance_size"] 
az_ml_initial_capacity  = cfg["azureml_endpoint_autoscale_settings"]["initial_capacity"] 
az_ml_autoscale_metric  = cfg["azureml_endpoint_autoscale_settings"]["metric"] 
az_ml_autoscale_scale_in_threashold  = cfg["azureml_endpoint_autoscale_settings"]["scale_in_threashold"] 
az_ml_autoscale_scale_out_threashold = cfg["azureml_endpoint_autoscale_settings"]["scale_out_threashold"] 
