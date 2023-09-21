source functions.sh

#THE AZURE ML PYTHON SDK NEEDS A SERVICE PRINCIPAL FOR AUTHENTICATION
#THIS SCRIPT WILL CHECK IF A PRINCIPAL EXISTS AND IT IS UP TO DATE
#IF NOT, IT WILL CREATE ONE 
#AFTER THIS, GLOBAL ENVIRONMENTS MUST BE CREATED
echo "INFO: This script shall be executed in the following way or ENV VARS will not be exported: '. 0_get_principal.sh'"

#Check config.yaml file exists
if [ ! -f config.yaml ]
then
    echo "ERROR: config.yaml does not exist."
    exit
fi

#Check it is not empty
if [ ! -s config.yaml ]
then
    echo "ERROR: config.yaml is empty."
    exit
fi

#Check credential file is added in config
new_principal_needed="False"
credentials_file=$(get_configuration_item "credentials_file")
if [[ ! -f $credentials_file ]]
then
    echo "WARNING: Credential file in config.yaml does not exist"
    new_principal_needed="True"
else
    #Check credential file
    AZURE_CLIENT_ID=$(jq     -r .appId    $credentials_file)
    AZURE_TENANT_ID=$(jq     -r .tenant   $credentials_file)
    AZURE_CLIENT_SECRET=$(jq -r .password $credentials_file)

    #If any of the variables is not set, we need a new principal
    if [ $AZURE_CLIENT_ID = "null" ] || [ $AZURE_TENANT_ID = "null" ] || [ $ = "null" ]
    then
        echo "WARNING: Principal information not available in principal file"
        new_principal_needed="True"
    fi


    #If we are not able to retrieve an access token, we need a new principal
    access_token=$(curl -s "https://login.microsoftonline.com/$AZURE_TENANT_ID/oauth2/token" -H "Content-Type: application/x-www-form-urlencoded" --data "grant_type=client_credentials&client_id=$AZURE_CLIENT_ID&client_secret=$AZURE_CLIENT_SECRET&resource=https%3A%2F%2Fmanagement.core.windows.net%2F" | jq -r ".access_token" )
    if [ $access_token"a" = "nulla" ] || [ $access_token"a" = "a" ]
    then
        echo "WARNING: Not able to retrieve an access token with existing principal"
        new_principal_needed="True"
    fi
fi

if [ $new_principal_needed = "True" ]
then
    echo "WARNING: New principal is needed"

    if [ $(az_cli_installed) -eq 0 ]
    then
        echo "AZ CLI installed"
    else
        echo "AZ CLI not installed. Installing Az CLI"
        curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
    fi

    subscription_id=$(get_configuration_item "subscription_id")
    principal_name=$(get_configuration_item "principal_name")

    az ad sp create-for-rbac --name $principal_name --role Contributor --scopes "/subscriptions/$subscription_id" > $credentials_file
    
    AZURE_CLIENT_ID=$(jq     -r .appId    $credentials_file)
    AZURE_TENANT_ID=$(jq     -r .tenant   $credentials_file)
    AZURE_CLIENT_SECRET=$(jq -r .password $credentials_file)

else
    echo "INFO: Principal is up to date"
fi

export AZURE_CLIENT_ID=$AZURE_CLIENT_ID
export AZURE_TENANT_ID=$AZURE_TENANT_ID
export AZURE_CLIENT_SECRET=$AZURE_CLIENT_SECRET

