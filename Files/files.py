import os

def getFilesInWorkingDir(workingPath):
    """
    Args:
        workingPath (str): actual dir to scan for files.
    Description:
        Check files in working directory wd
    """
    filesInWorkingDir = [file for file in os.listdir(workingPath) if os.path.isfile(file)] 
    return filesInWorkingDir