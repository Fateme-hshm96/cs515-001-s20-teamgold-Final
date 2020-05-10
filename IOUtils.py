import pickle
import os

def writeBugMap(projectMap,outputDir):
   if not os.path.exists(outputDir): os.makedirs(outputDir)
   for project in projectMap:
      with open(outputDir + "/" + str(project) + "_bug_fixing_commits", 'wb') as project_file:
         temp_dict = {}
         temp_dict[project] = projectMap[project]
         pickle.dump(temp_dict, project_file)

# def readBugMap(projectMap,inputDir):
