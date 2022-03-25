import numpy as np
import pandas as pd
import sys

#%% CLASS PROJECT
class projects:
    def __init__(self, que, projectName, piority, client, owner, stage, startDate, finishDate, enagmenment, description):
        self.que = que
        self.projectName = projectName
        self.piority = piority
        self.client = client
        self.owner = owner
        self.stage = stage
        self.startDate = startDate
        self.finishDate = finishDate
        self.enagmenment = enagmenment
        self.description = description

    def getProjectList(self):
        return [
            self.que,
            self.projectName,
            self.piority,
            self.client	,
            self.owner		,
            self.stage		,
            self.startDate	,
            self.finishDate ,
            self.enagmenment,
            self.description
        ]
    def getProjectPercentage(self):
        projectStages = ['Need', 'Preeliminary' ,'Pending' ,'Manufacturing' ,'Validation' ,'Verification' ,'Delivery'
                         ,'Support']
        projectWeights = [0, 5, 0, 60, 10, 10, 5, 10]
        projectWeightsFinish = []
        for i, weight in enumerate(projectWeights):
            if(i < len(projectWeights) and i> 0):
                projectWeightsFinish.append(projectWeightsFinish[i - 1] + weight)
            elif (i == 0):
                projectWeightsFinish.append(weight)

        keyOfWeights = dict(zip(projectStages, projectWeightsFinish))
        return keyOfWeights[self.stage]

    def getProjectDict(self):
        return {
            'Que':self.que,
            'ProjectName': self.projectName,
            'Piority': self.piority,
            'Customer': self.client,
            'Owner': self.owner,
            'Stage': self.stage,
            'Start': self.startDate,
            'Finish': self.finishDate,
            'Resources': self.enagmenment,
            'Description': self.description
        }

    def getProjectDF(self):
        return {
            'Que':[self.que,],
            'ProjectName': [self.projectName, ],
            'Piority': [self.piority, ],
            'Customer': [self.client, ],
            'Owner': [self.owner, ],
            'Stage': [self.stage, ],
            'Status': [self.getProjectPercentage(), ],
            'Start': [self.startDate, ],
            'Finish': [self.finishDate, ],
            'Resources': [self.enagmenment, ],
            'Description': [self.description, ],
        }

    def printProjectInfo(self):
        print(
            "{}. BJ10 piority: {}. \nProject {} for {}. \nResponsible developer {} as resurses {}%, work on project on step {}. \nProject start: \t {}, finish: \t {}. \nDescription: {}".format(
            self.que,
            self.piority,
            self.projectName,
            self.client	,
            self.owner		,
            self.enagmenment *100,
            self.stage		,
            self.startDate	,
            self.finishDate ,
            self.description
        ))

def getSetUp():
    piorityList = [1, 2, 3]
    projectStages = ['Need', 'Preeliminary','Pending','Manufacturing','Validation','Verification','Delivery','Support']
    projectWeights = [0, 5, 0, 60, 10, 10, 5, 10]
    ownersList = ['Michal Debosz']
    clientsList = list(pd.read_excel('ProjectReview.xlsx')['Customer'].unique())
    return piorityList, projectStages, projectWeights, ownersList, clientsList


def addNewProject():
    piorityList, projectStages, projectWeights, ownerList, clientList = getSetUp()
    print("Que: ", end="")
    que = int(input())
    print("Project name: ", end="")
    name = str(input())
    print("\nPiority {}: ".format(str(piorityList)), end="")
    piority = int(input())
    print("\nCustomers fex.: {}: ".format(str(clientList)), end="")
    cust = str(input())
    print("\nOwner fex.: {}: ".format(str(ownerList)), end="")
    owner = str(input())
    print("\nProject Stage: {}: ".format(str(projectStages)), end="")
    projectStages = str(input())
    print("\nStart date YYYY-MM-DD: ", end="")
    st = str(input())
    print("\nFinish date YYYY-MM-DD: ", end="")
    ed = str(input())
    print("\nPercentage of resources[0-1]: ", end="")
    prc = float(input())
    print("\nNote: ", end="")
    note = str(input())

    projectTemplate = projects(que,
                               name,
                               piority,
                               cust,
                               owner,
                               projectStages,
                               st,
                               ed,
                               prc,
                               note)
    return pd.DataFrame(data=projectTemplate.getProjectDF())

def testProject():
    piorityList, projectStages, projectWeights, ownersList, clientsList = getSetUp()
    project1 = projects(100,
                        'Automated-Classification-ABC',
                        piorityList[0],
                        clientsList[0],
                        ownersList[0],
                        projectStages[3],
                        '2021-01-01',
                        '2021-01-01',
                        1,
                        """Automatic script based on excel logic with requirements regarding to business.""")
    project1.printProjectInfo()
    return project1.getProjectDF()

def displayInformations():
    print("--- Python editor of current project ---")
    print("Display project names: dpn")
    print("Remove project: rmp {ProjectName}")
    print("Edit project parameters: e {ProjectName}")
    print("Add project: a")
    print('Exit - 0')
    print("--- ------------------------------------") 

def toExcel(df):
    """Save the excel fith projects"""
    df.sort_values(by=['Que','Piority','Status','Finish'], ascending=[True, True, False, False]).to_excel('ProjectReview.xlsx', index=False)

def openFile():
    """Open the excel fith projects"""
    return pd.read_excel('ProjectReview.xlsx', index_col=None)

def switcher(command):
    try:
        projectBook = openFile()
        if command[0] == 'dpn':
            print(str(projectBook["ProjectName"]))
        elif command[0] == 'rmp':
            if command[1] in list(projectBook["ProjectName"]):
                projectBook = projectBook[projectBook["ProjectName"] != command[1]]
                toExcel(projectBook)
                print("Deleted {}".format(command[1]))
            else:
                print("No {} project".format(command[1]))

        elif command[0] == 'e':
            if command[1] in list(projectBook["ProjectName"]):
                print("Columns: {}".format(str(projectBook.columns)))
                print("Input: Column NewValue")
                if len(command)<3:
                    dat = input()
                    commandForEdit = dat.split()
                else:
                    commandForEdit = [command[2], command[3]]
                if commandForEdit[0] in list(projectBook.columns):
                    currentProjectToEdit = projectBook[projectBook['ProjectName'] == command[1]]
                    projectBook = projectBook[projectBook['ProjectName'] != command[1]]
                    try:
                        currentProjectToEdit[commandForEdit[0]] = int(commandForEdit[1])
                    except:
                        currentProjectToEdit[commandForEdit[0]] = str(commandForEdit[1])
                    projectBook = projectBook.append(currentProjectToEdit)
                    toExcel(projectBook)
                    print("Ok, edited!")
                else:
                    print("Wrong column name '{}'".format(commandForEdit[0]))
            else:
                print("No {} project".format(command[1]))
        elif command[0] == 'a':
            projectBook = projectBook.append(addNewProject())
            projectBook.reset_index(drop=True)
            toExcel(projectBook)
            print("OK, saved!")

    except IndexError:
        print("Index Error")

def main():
    x = 1
    if(len(sys.argv) < 1):
        while (x != '0'):
            print("Command: ", end='')
            x = input()
            command = x.split()
            try:
                switcher(command)
            except IndexError:
                print("Index Error")

        print("Exit")
    else:
        try:
            command = sys.argv
            switcher(command[1:])
        except IndexError:
            print("Error")

#%% Body
displayInformations()
main()

