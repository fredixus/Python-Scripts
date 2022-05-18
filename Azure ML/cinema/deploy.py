'''
This file is designed to deploy a model to azure ml as an endpoint
'''

# TODO: update this script to take arguments from the command line
# to specify models, webservice names etc.

from azureml.core.model import Model
from azureml.core import Workspace
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AksWebservice, AciWebservice, LocalWebservice
from azureml.core.authentication import AzureCliAuthentication
from azureml.core.compute import ComputeTarget, AksCompute
from azureml.exceptions import ComputeTargetException
from get_env import get_azureml_environment

root = "/"

cli_auth = AzureCliAuthentication()
# define the workspace
ws = Workspace(
    subscription_id=SUBSCRIPTION,
    resource_group="test_rg",
    workspace_name="test-ml",
    #auth=cli_auth
)

# Choose a name for your cluster
compute_name = "testvm"

# Check to see if the cluster already exists
try:
    compute_target = ComputeTarget(workspace=ws, name=compute_name)
    print('Found existing compute target')
except ComputeTargetException:
    print('Creating a new compute target...')
    # Provision AKS cluster with GPU machine
    prov_config = AksCompute.provisioning_configuration(vm_size="Standard_NC6")

    # Create the cluster
    compute_target = ComputeTarget.create(
        workspace=ws, name=compute_name, provisioning_configuration=prov_config
    )

    compute_target.wait_for_completion(show_output=True)

inference_config = InferenceConfig(
    environment=get_azureml_environment(),
    source_directory=root,
    entry_script='model.py',
)

#deployment_config = LocalWebservice.deploy_configuration(port=6789)
deployment_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=2)
"""deployment_config = AksWebservice.deploy_configuration(
    autoscale_enabled=False,
    num_replicas=1,
    gpu_cores=1,
    cpu_cores=1,
    memory_gb=8
)"""

deployment_name = 'example-deployment'

service = Model.deploy(
    workspace=ws,
    name=deployment_name,
    models=[],
    inference_config=inference_config,
    deployment_config=deployment_config,
    deployment_target=compute_target,
    overwrite=True,
    show_output=True
)

service.wait_for_deployment(show_output=True)

print(service.get_logs())
print(service.scoring_uri)
