from azure.identity import DefaultAzureCredential

def log(message):
    print(message)

def get_az_credentials():
    credentials = DefaultAzureCredential()
    credentials.get_token("https://management.azure.com/.default")

    return credentials