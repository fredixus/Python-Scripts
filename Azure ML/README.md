# Description of infrastructure

ML project, can be devided in the 3 layers of the infrastructure.
The first layer is data. The first layer is a representation of data sources used in projects such as SQL databases, or flat files (CSV, XLSX, Jason).
The second layer is learning and development. This layer includes scripts to deliver the model, model development, implementation of model API, and deployment script.
The third layer is a production API with compute instance. This layer menage request and return model output.

## General infrastructure graph

![General](/general.png "General infrastructure graph")
`Graph 1`
The extra layer is a DevOps platform to track all changes and follow the newest code version for all developers.

## Azure infrastructure graph

![Azure](/azure.png "Azure infrastructure graph")
`Graph 2`
For all typical use cases, our cloud infrastructure could be constructed as in the above image.
A good practice is to create a new resource group for the project.
For a new resource group created for the ML project we can define two main services:

- obligatory (ML service, Storage Account, Key Vault)
- optional (Azure SQL)
The creation of a new project should be started by creating a new resource group and then an ML service.

Step by step Machine Learning service set-up:

1. Select new Resource group
2. Create new resource **Machine Learning**
![Screen1](/screens/1.png "Screen1")

3. Select a **resource group**.
4. Specify: **Workspace name**, **Region**, **Storage account**, **Key vault**, **Application insights**.
5. Create new or select already created **Container registry**.
![Screen2](/screens/2.png "Screen2")

6. Create new service:  
![Screen4](/screens/4.png "Screen4")

7. Summary:
![Screen5](/screens/5.png "Screen5")

8. After creating:
![Screen6](/screens/6.png "Screen6")

## Conceptual project graph

The following graph includes the typical structure of tools, services, and products used for project implementation.
This stage reference to Layer II and Layer III in `Graph 1`.
![Conceptual](/conceptual.png "Conceptual project graph")
`Graph 3`

1. As data source we use files or databases
2. To learn we use Python/R scripting as an output of this stage is a model file (pt/pkl/model/others)
3. To create API handler and deploy the model we use Python script
*Test*
4. Deployment of model on local machine to test input->output
*Production*
5. After tests model needs to be deployed into the cloud environment.

## Files in projects

The following graph includes the typical structure of files in a project. This stage reference to Layer II in `Graph 1`.

![Files](/files.png "Files")
`Graph 4`

`tip: all graphs you can use for other projects.`
