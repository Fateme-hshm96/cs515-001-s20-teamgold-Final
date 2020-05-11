import pickle
import os

def writeBugMap(projectMap,outputDir,fileEnding):
   if not os.path.exists(outputDir): os.makedirs(outputDir)
   for project in projectMap:
      with open(outputDir + "/" + str(project) + str(fileEnding), 'wb') as project_file:
         temp_dict = {}
         temp_dict[project] = projectMap[project]
         pickle.dump(temp_dict, project_file)

def readBugMap(projectMap,inputDir):
   for filename in os.listdir(inputDir):
      path = str(inputDir) + "/" + str(filename)
      with open(path, 'rb') as buggy_commits_file:
         temp_map = pickle.load(buggy_commits_file)
         for project,commits in temp_map.items():
            projectMap[project] = commits