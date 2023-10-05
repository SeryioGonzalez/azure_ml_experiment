import urllib.request
import json
import os
import ssl

import azml_config as cfg
import az_utils as utils
from azure.ai.ml import MLClient
from random import randint

utils.log("INFO: Getting credentials")
credential = utils.get_az_credentials()

#INITIALIZE AZ ML CLIENT
utils.log("INFO: Initializing AzML Client")
ml_client = MLClient(credential, cfg.az_subscription_id, cfg.az_resource_group, cfg.az_ml_workspace_name)

endpoint_url = f"https://{cfg.az_ml_online_endpoint}.{cfg.az_region}.inference.ml.azure.com/score"
online_endpoint_keys = ml_client.online_endpoints.get_keys(name=cfg.az_ml_online_endpoint)
endpoint_primary_key = online_endpoint_keys.primary_key

data =  {
  "input_data": {
    "columns": [
      "sepal_length", "sepal_width", "petal_length", "petal_width"
    ],
    "index": [0],
    "data": [
      [5.4, 3.9, 1.7, 0.4]
    ]
  }
}

headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ endpoint_primary_key), 'azureml-model-deployment': cfg.az_ml_deployment_name }
body = str.encode(json.dumps(data))

while True:
  request_id = randint(0, 1000000)
  request    = urllib.request.Request(endpoint_url, body, headers)

  try:
      response = urllib.request.urlopen(request)

      result = response.read().decode("utf-8")
      print(f"Response for {request_id} is {result}")
  except urllib.error.HTTPError as error:
      print("The request failed with status code: " + str(error.code))
      print(error.info())
      print(error.read().decode("utf8", 'ignore'))