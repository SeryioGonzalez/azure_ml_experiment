
get_configuration_item () {
    config_value=$(grep $1 config.yaml | awk '{print $2}')

    if [ $config_value = "" ]
    then
        echo "ERROR: $1 not in config.yaml"
        exit
    fi

    echo $config_value
    
}

az_cli_installed (){
    az --version &> /dev/null
    if [ $? -eq 0 ]
    then
        echo 0
    else
        echo 1
    fi

}