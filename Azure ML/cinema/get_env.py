'''
single function to insert ado pat into an env.yml file
for azure ml to enable installation of internal libraries
'''

import re
import os
import yaml
from azureml.core import Environment
from azureml.core.environment import DEFAULT_GPU_IMAGE
#from WoodProjectRoot import WoodProjectRoot as wpr

root = "/Users/mdebosz/Documents/Wood/MLOps_Orgin/MLOps/"

def get_azureml_environment():

    # read environment.yml and find replace env variables
    with open(root + "environment.yml", "r") as stream:
        env_file = yaml.safe_load(stream)

    deps = env_file['dependencies']

    # find the location where we start to define pip deps
    for idx, val in enumerate(deps):
        if isinstance(val, dict):
            dep_idx = idx
    # the strucutre of this dict is as follows:
    # key = 'pip'
    # value = list of packages and their versions
    # we need to find locations of the structure ${}
    # inside the ${} will be an environment variable name
    # get that from your environment and replace the ${} with the variable value

    packages = deps[dep_idx]['pip']
    pattern = r'\${.*}'
    for idx, val in enumerate(packages):
        re_match = re.search(pattern, val)
        if bool(re_match):
            # get the env variable name
            var_name = re_match.group(0)
            # the first two elements of the string and the last element need to be removed
            env_var_name = var_name[2:-1]

            env_val = os.environ[env_var_name]

            new_package = re.sub(pattern, env_val, val)
            # replace the package description inlace
            packages[idx] = new_package

    # re-define the packages we want
    deps[dep_idx]['pip'] = packages

    env_file['dependencies'] = deps

    # write the new dependencies to file
    # NOTE: This file must be deleted after use
    with open(root + 'custom_env.yml', 'w') as outfile:
        yaml.dump(env_file, outfile, default_flow_style=False)

    myenv = Environment.from_conda_specification(name = 'env', file_path = root + 'custom_env.yml')
    myenv.inferencing_stack_version = 'latest'
    env = {}
    myenv.environment_variables = env
    myenv.docker.base_image = DEFAULT_GPU_IMAGE

    os.remove(root + 'custom_env.yml')

    return myenv